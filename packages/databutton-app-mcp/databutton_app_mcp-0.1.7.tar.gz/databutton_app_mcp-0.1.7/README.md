# Databutton App MCP

Use API endpoints from your Databutton app as LLM tools from any MCP compatible client!

This is a simple proxy that runs locally and connects securely to your Databutton app
using the MCP protocol over websockets.

To use it, make sure you have uv installed, see instructions here if not:

    https://docs.astral.sh/uv/getting-started/installation/

First download an API key from the settings page of your Databutton app, and save it to a file.

Then configure your LLM client (e.g. Claude Desktop or Cursor), like this:

```json
{
  "mcpServers": {
    "myDatabuttonApp": {
      "command": "uvx",
      "args": [
        "databutton-app-mcp"
      ],
      "env": {
        "DATABUTTON_API_KEY": "YOUR-DATABUTTON-APP-KEY"
      }
    }
  }
}
```

Here DATABUTTON_API_KEY is either the api key or the path to a file containing it.
You can download the API key for your Databutton app on the app settings page.
Make sure to keep it secure and don't share it.
