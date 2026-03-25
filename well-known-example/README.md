# well-known-example

Copy `mcp-server` to your webroot at `.well-known/mcp-server` to expose your MCP server.

```bash
cp mcp-server /var/www/html/.well-known/mcp-server
```

Edit the fields to match your server. Minimum required fields:

```json
{
  "mcp_version": "2025-06-18",
  "name": "Your Server Name",
  "endpoint": "https://yourdomain.com/mcp",
  "transport": "http"
}
```
