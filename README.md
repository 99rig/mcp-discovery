# mcpstandard.dev

**The `mcp://` URI Scheme and MCP Server Discovery Mechanism**

Reference implementation and specification for [draft-serra-mcp-discovery-uri-03](https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/03/) — the latest version.

---

## What is this?

This repository contains:

- The IETF Internet Draft defining `mcp://` as a URI scheme for MCP server discovery
- A live reference implementation at [mcpstandard.dev](https://mcpstandard.dev)
- A Python client library for resolving `mcp://` URIs
- A validator for `/.well-known/mcp-server` manifests

## The Problem

Today, connecting an AI agent to an MCP server requires manual configuration.
No standard mechanism exists for an agent to discover which web domains expose
an MCP server starting from a domain name alone.

## The Solution

Three components work together:

1. **`mcp://` URI scheme** — identifies an MCP server by domain
2. **`/.well-known/mcp-server`** — a JSON manifest exposing server metadata  
3. **DNS TXT fallback** — `_mcp.domain TXT "v=mcp1; endpoint=..."`

## Quick Start — Expose your MCP server

```bash
mkdir -p .well-known
echo '{
  "mcp_version": "2025-06-18",
  "name": "My MCP Server",
  "endpoint": "https://mydomain.com/mcp",
  "transport": "http"
}' > .well-known/mcp-server
```

## Quick Start — Resolve an mcp:// URI

```bash
# Step 1 — well-known
curl -sf https://domain.com/.well-known/mcp-server

# Step 2 — DNS fallback
dig +short TXT _mcp.domain.com

# Step 3 — direct
curl -X POST https://domain.com/mcp
```

## Live Reference Implementation

```bash
curl -s https://mcpstandard.dev/.well-known/mcp-server | python3 -m json.tool
```

## IETF Draft

| Version | URL |
|---------|-----|
| -00 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/00/ |
| -01 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/01/ |
| -02 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/02/ |
| **-03** | **https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/03/** ← latest |

## Related Work

- [SEP-1649](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1649) — MCP Server Cards proposal by MCP maintainers
- [GitHub Discussion #2462](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2462) — Coordination thread

## Author

Marco Serra — Mumble Group — Milan, Italy  
marco.serra@mumble.group | https://mcpstandard.dev
