# Document 1 — The Problem

## Background: what is MCP

The Model Context Protocol (MCP) is an open protocol published by Anthropic in November 2024. It defines a standard JSON-RPC 2.0 interface that allows AI agents to connect to external tools and services — called "MCP servers" — to read data, execute actions, and query structured resources.

An MCP server exposes three types of primitives:
- **Tools** — functions executable by the agent (e.g. `search_products`, `send_email`)
- **Resources** — readable data as context (e.g. documents, catalogs, databases)
- **Prompts** — reusable templates for standardized workflows

MCP is already adopted by Claude (Anthropic), GitHub Copilot, Cursor, VS Code, and dozens of other AI clients. The number of public MCP servers exceeds thousands and is growing rapidly.

---

## Current state of MCP discovery

Despite the rapid growth of the ecosystem, no standard mechanism exists that allows an AI agent to **autonomously discover** which websites or services expose an MCP server.

The only current way to connect an AI agent to an MCP server is **manual configuration**: someone must know the server exists, know its URL, and explicitly configure it in the AI client. This creates a structural dependency on human knowledge that prevents autonomous automation.

---

## Why manual registries are not enough

Directories like `registry.modelcontextprotocol.io`, `mcp.so`, and the GitHub registry exist. However they have structural limitations:

- They require **voluntary registration** by the server operator — those who don't know they exist never register
- They are **manually updated** and therefore by definition incomplete and potentially outdated
- No mechanism exists to automatically verify that registered servers are still active
- They work like Yellow Pages: you register and hope to be found
- An AI agent does not consult them automatically — it depends on the client configuration
- They don't cover the **long tail** — thousands of small, vertical servers that never register

The fundamental problem is that registries require an active action by the server operator. A robust discovery mechanism must work even without this action.

---

## Why web search is not enough

An AI agent can use web search tools (Google, Bing, Brave) to find information. But web search is designed for humans, not agents:

- Search engines index **HTML text**, not MCP endpoints
- No semantic signal exists in the web that says "this site exposes an MCP server"
- Even finding a relevant site, the agent doesn't know if it exposes MCP, on which path, with what authentication
- The result is unstructured text to interpret, not a directly queryable endpoint
- The latency of a web search query is incompatible with real-time discovery

---

## The gap that exists today

```
HUMAN searches "stainless M6 bolts where to buy"
  → Google indexes sites
  → finds bolts.com
  → HTML page with prices and catalog

AI AGENT searches "stainless M6 bolts where to buy"
  → web search → finds bolts.com → reads HTML → interprets text
  → DOESN'T KNOW that bolts.com has an MCP server with structured catalog
  → CANNOT directly query stock, prices, availability in real time
  → responds with approximate information extracted from text
```

The gap is precise: **no protocol exists that allows an AI agent to automatically discover an MCP server starting from a web domain**, nor an infrastructure that indexes such servers in a queryable way.

Three elements are simultaneously missing:
1. A standard **URI scheme** to identify MCP servers (`mcp://`)
2. A **discovery convention** to expose server metadata (`/.well-known/mcp-server`)
3. A **crawler** that automatically indexes exposed MCP endpoints

---

## Who is interested in solving it

**Supply side — who exposes MCP servers**
- E-commerce site operators (WooCommerce, Shopify) → want to be found by AI agents just as they want to be found by Google today
- API and structured data providers → want their services to be queryable by agents without custom integrations
- Companies with internal knowledge bases → want to expose data to their AI agents in a standardized way

**Demand side — who uses MCP servers**
- AI agent developers → want to query services without manual configuration for each new service
- AI platforms (Anthropic, OpenAI, Google, Microsoft) → want an open, non-proprietary tool discovery ecosystem
- End users → want AI agents that autonomously find the necessary resources

**Standards side**
- IETF and W3C → interest in standardizing before incompatible proprietary solutions emerge

---

## Requirements for a solution

**R1 — Decentralization**: No mandatory central authority. Anyone must be able to expose an MCP server without depending on a third-party registry.

**R2 — Automatic discovery**: An AI agent must be able to discover an MCP server starting only from the web domain, without manual configuration.

**R3 — Verifiability**: The agent must be able to verify that the declared MCP server actually belongs to the indicated domain.

**R4 — Explicit opt-out**: Operators must be able to explicitly indicate they do not want to be indexed.

**R5 — Compatibility with existing infrastructure**: DNS, HTTPS, `.well-known` — no new network infrastructure required.

**R6 — Implementation simplicity**: Ideally a single static JSON file.

---

## Non-goals

- The MCP protocol itself — already defined by the Anthropic specification
- Authentication between agent and MCP server — already covered by OAuth 2.1 in the MCP spec
- The format of tools, resources and prompts — already defined in the MCP spec
- Security of operations performed via MCP — server's responsibility
- Discovery of MCP servers on private networks or corporate intranets

---

## Historical analogy

Before search engines, websites existed but were invisible — you knew a site only if someone told you. Google solved the web discovery problem with three components:

1. A standard protocol (HTTP) that all sites already used
2. A crawler that followed links automatically without requiring action from operators
3. A queryable index that returned relevant results

`mcp://` + `/.well-known/mcp-server` + an MCP crawler is the same architecture applied to the AI agent ecosystem. The difference is that the recipients are not humans searching for web pages, but AI agents searching for tools to use.

The historical moment is analogous to 1993 — the web existed, sites existed, but the discovery layer that made them autonomously navigable was still missing.

---

*Next document: Document 2 — The Technical Proposal*
