# Databutton App MCP

Use API endpoints from your Databutton app as LLM tools from any MCP compatible client!

This is a simple proxy that runs locally and connects securely to your Databutton app
using the MCP protocol over websockets.

First download an API key from the settings page of your Databutton app, and save it to a file.

For example say you downloaded a key file named `MY-DATABUTTON-APP-KEYID.json`,
and save it to the directory `~/.config/databutton/mcp-keys/`.

Then to add this app to clients such as Claude Desktop, add the following to your client MCP settings or config file:

```json
{
  "mcpServers": {
    "my-databutton-app": {
      "command": "uvx",
      "args": [
        "databutton-app-mcp"
      ],
      "env": {
        "DATABUTTON_MCP_API_KEY": "~/.config/databutton/mcp-keys/MY-DATABUTTON-APP-KEYID.json"
      }
    }
  }
}
```

Here DATABUTTON_MCP_API_KEY either refers to the full path of the api key file you stored,
or it can be the api key value itself.
Either way one api key gives access to endpoints of one Databutton app.
