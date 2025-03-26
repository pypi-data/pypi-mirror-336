import argparse
import pathlib
import base64
import json
import asyncio
import signal
import sys
import os
import logging

from websockets import Subprotocol, connect
from websockets.asyncio.client import ClientConnection

logger = logging.getLogger("databutton-app-mcp")

logging.basicConfig(
    level=logging.WARNING,
    format="databutton-app-mcp %(levelname)s: %(message)s",
    stream=sys.stderr,
)


async def stdin_to_ws(websocket: ClientConnection):
    """Read from stdin and send to websocket"""
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:  # EOF
            break
        await websocket.send(line.rstrip("\n"))


async def ws_to_stdout(websocket: ClientConnection):
    """Receive from websocket and write to stdout"""
    async for msg in websocket:
        print(msg, flush=True)


async def run_ws_proxy(uri: str, bearer: str | None = None):
    logger.info(f"Connecting to mcp server at {uri}")

    # Set up signal handling for graceful exit
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, loop.stop)

    auth_headers: list[tuple[str, str]] = []
    if bearer:
        auth_headers.append(("Authorization", f"Bearer {bearer}"))

    auth_subprotocols: list[Subprotocol] = []
    # auth_subprotocols.append(Subprotocol(f"Authorization.Bearer.{bearer}"))

    try:
        async with connect(
            uri,
            subprotocols=[Subprotocol("mcp")] + auth_subprotocols,
            additional_headers=auth_headers,
        ) as websocket:
            logger.info("Connection established")

            stdin_task = asyncio.create_task(stdin_to_ws(websocket))
            stdout_task = asyncio.create_task(ws_to_stdout(websocket))

            try:
                await asyncio.gather(stdin_task, stdout_task)
            except asyncio.CancelledError:
                logger.error("Connection terminated")
            finally:
                stdin_task.cancel()
                stdout_task.cancel()
    except Exception as e:
        logger.error(f"Closing with error: {e}")


def parse_apikey(apikey: str) -> dict[str, str]:
    if not apikey:
        raise ValueError("API key must be provided")

    try:
        decoded = base64.urlsafe_b64decode(apikey).decode()
        return json.loads(decoded)
    except Exception:
        pass

    try:
        decoded = base64.b64decode(apikey).decode()
        return json.loads(decoded)
    except Exception:
        pass

    try:
        return json.loads(apikey)
    except Exception:
        pass

    raise ValueError("Invalid API key")


DATABUTTON_API_KEY = "DATABUTTON_API_KEY"


def main():
    logger.info("Starting Databutton app MCP proxy")
    try:
        parser = argparse.ArgumentParser(
            description="Expose Databutton app endpoints as LLM tools with MCP over websocket"
        )
        parser.add_argument(
            "-k",
            "--apikeyfile",
            dest="apikeyfile",
            type=str,
            help="File containing API key to use",
            required=False,
        )
        args = parser.parse_args()

        env_apikey = os.environ.get(DATABUTTON_API_KEY)

        if not (args.apikeyfile or env_apikey):
            logger.error("No API key provided")
            sys.exit(1)

        if args.apikeyfile and pathlib.Path(args.apikeyfile).exists():
            logger.info(f"Using api key from file {args.apikeyfile}")
            apikey = pathlib.Path(args.apikeyfile).read_text()
        else:
            logger.info("Using api key from environment variable")
            apikey = env_apikey

        if not apikey:
            logger.error("Provided API key is blank")
            sys.exit(1)

        claims: dict[str, str] = {}
        try:
            claims = parse_apikey(apikey)
        except Exception as e:
            logger.error(f"Failed to parse API key: {e}")
            sys.exit(1)

        uri = claims.get("uri")
        if not uri:
            logger.error("URI must be provided")
            sys.exit(1)

        if not (
            uri.startswith("ws://localhost")
            or uri.startswith("ws://127.0.0.1:")
            or uri.startswith("wss://")
        ):
            logger.error("URI must start with 'ws://' or 'wss://'")
            sys.exit(1)

        # TODO: Exchange refresh token for access token here
        accessToken: str | None = claims.get("accessToken")
        if claims.get("refreshToken"):
            pass

    except Exception as e:
        logger.error(f"Error while parsing input: {e}")
        sys.exit(1)

    try:
        asyncio.run(
            run_ws_proxy(
                uri=uri,
                bearer=accessToken,
            )
        )
    except KeyboardInterrupt:
        logger.error("Program terminated")
        sys.exit(1)


if __name__ == "__main__":
    main()
