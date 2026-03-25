# Document 3 — The Crawler

## What is the MCP crawler

The MCP crawler is an automated system that scans the web for exposed MCP servers, indexes them, and makes their capabilities queryable by AI agents.

It is the equivalent of Googlebot — but instead of indexing HTML pages for humans, it indexes MCP endpoints for machines.

---

## How it finds sites with MCP endpoints

The crawler operates on multiple fronts in parallel:

```
SOURCE 1 — /.well-known scan
  List of known domains (Alexa top 1M, Common Crawl)
  For each domain: GET https://domain/.well-known/mcp-server
  If valid JSON response → index

SOURCE 2 — DNS TXT records
  DNS query: _mcp.domain
  If TXT record present with v=mcp1 → index

SOURCE 3 — Existing registries
  Import from registry.modelcontextprotocol.io
  Import from mcp.so, smithery.ai, GitHub registry
  Verify that endpoints are still active

SOURCE 4 — Voluntary submission
  Public API to register mcp://mydomain.com
  Verify ownership via DNS challenge or HTTP challenge
  Analogous to Google Search Console

SOURCE 5 — Links in the web
  Scan HTML pages looking for:
  <link rel="mcp-server" href="/.well-known/mcp-server">
  Analogy: how RSS feeds were discovered via <link rel="alternate">
```

---

## How it indexes capabilities

Once an endpoint is found, the crawler follows this process:

```
PHASE 1 — Manifest reading
  GET https://domain/.well-known/mcp-server
  Extracts: name, description, endpoint, transport, categories

PHASE 2 — MCP connection
  POST endpoint/mcp (initialize handshake)
  tools/list      → list tools with name, description, JSON schema
  resources/list  → list available resources
  prompts/list    → list prompt templates

PHASE 3 — Semantic indexing
  Generate vector embedding for each tool
  (based on name + natural language description)
  Store in pgvector for semantic search

PHASE 4 — Categorization
  Assign categories from predefined taxonomy:
  e-commerce, finance, health, legal, logistics,
  knowledge-base, dev-tools, media, travel, ...
  Combine categories declared in manifest
  with categories inferred from tools

PHASE 5 — Periodic update
  Ping every 24h to verify server is active
  Re-index if last_updated field changes
  Remove from index if server unresponsive for 7 days
```

---

## The Search API — complete specification

The index built by the crawler is exposed via a **REST Search API** that an AI agent can query directly.

### Endpoint

```
GET /v1/search
```

### Query parameters

| Parameter | Type | Requirement | Description |
|---|---|---|---|
| `q` | string | MUST | Natural language query or keywords |
| `category` | string | MAY | Category filter (e.g. `e-commerce`) |
| `country` | string | MAY | Geographic filter (ISO 3166-1, e.g. `US`) |
| `language` | string | MAY | Language filter (ISO 639-1, e.g. `en`) |
| `auth` | string | MAY | Auth filter: `none`, `apikey`, `oauth2` |
| `limit` | integer | MAY | Number of results (default: 10, max: 50) |
| `offset` | integer | MAY | Pagination (default: 0) |

### Example request

```http
GET /v1/search?q=bolts+screws+fasteners&category=e-commerce&country=US&limit=5
Accept: application/json
```

### Response format

```json
{
  "query": "bolts screws fasteners",
  "total": 12,
  "limit": 5,
  "offset": 0,
  "results": [
    {
      "mcp_uri": "mcp://bolts.com",
      "name": "Bolts.com MCP Server",
      "description": "Catalog of bolts, screws and metal fasteners",
      "endpoint": "https://bolts.com/mcp",
      "transport": "http",
      "auth": "none",
      "categories": ["e-commerce", "hardware", "fasteners"],
      "languages": ["en"],
      "coverage": "US",
      "tools": [
        {
          "name": "search_products",
          "description": "Search products by type, material and size"
        },
        {
          "name": "check_stock",
          "description": "Check warehouse availability in real time"
        },
        {
          "name": "get_price",
          "description": "Get updated prices with volume discounts"
        }
      ],
      "relevance_score": 0.97,
      "last_verified": "2026-03-25T08:00:00Z"
    }
  ]
}
```

### Complete agent → user flow

```
User: "where can I buy stainless M6 bolts at the best price?"

STEP 1 — Agent queries the Search API
  GET /v1/search?q=M6+stainless+bolts&category=e-commerce&country=US

STEP 2 — Search API returns 3 relevant servers
  mcp://bolts.com        relevance: 0.97
  mcp://hardware.us      relevance: 0.91
  mcp://fasteners.eu     relevance: 0.84

STEP 3 — Agent connects in parallel to the 3 servers
  → calls search_products({type:"M6", material:"stainless"}) on each
  → receives prices, stock, delivery times in real time

STEP 4 — Agent compares and responds
  "Stainless M6 bolts available from 3 suppliers:
   - bolts.com: $0.09/unit, 500 in stock, 24h delivery
   - hardware.us: $0.08/unit, 200 in stock, 48h delivery
   - fasteners.eu: $0.10/unit, 1000 in stock, 24h delivery"
```

---

## Ranking algorithm

**1. Semantic relevance (weight 60%)**
Cosine distance between query embedding and indexed tool embeddings. Uses multilingual embedding models to support queries in languages different from the server language.

**2. Server quality (weight 25%)**
- Uptime over the last 30 days
- Average response time
- Manifest completeness (SHOULD fields present)
- Supported MCP version

**3. Contextual signals (weight 15%)**
- Geographic match with query country
- Language match
- Recency (last_updated date)

---

## Analogy with Googlebot

| Googlebot | MCP Crawler |
|---|---|
| Scans HTTP URLs | Scans domains for `/.well-known/mcp-server` |
| Indexes HTML text | Indexes MCP tools and capabilities |
| Responds to human queries via SERP | Responds to AI agent queries via Search API |
| PageRank + semantic ranking | Semantic + server quality ranking |
| `robots.txt` for exclusions | `"crawl": false` field in manifest |
| Google Search Console for registration | Voluntary submission API |

---

## Ethical crawler behavior and rate limiting

The crawler MUST respect the following rules:

```
- Respect the Cache-Control header of the manifest
- No more than 1 request every 10 seconds per domain
- Respect HTTP 429 (Too Many Requests) with exponential backoff
- Identify itself with User-Agent: MCPCrawler/1.0
- Only performs tools/list, resources/list, prompts/list — never tools/call
- Does not transmit sensitive data obtained during scanning
```

---

## Technical stack

```
Crawler
  → Python + asyncio        high concurrency, non-blocking I/O
  → aiohttp                 async HTTP client
  → dnspython               DNS queries for _mcp TXT records

Storage
  → PostgreSQL              server metadata and manifests
  → pgvector                vector embeddings for semantic search
  → Redis                   domain queue + cache

Search API
  → FastAPI                 REST endpoint /v1/search
  → sentence-transformers   multilingual embedding generation
  → uvicorn                 production-grade ASGI server

Infrastructure
  → cron job every 24h      server activity verification
  → worker pool             parallel domain scanning
  → cloud-native            horizontally scalable on Kubernetes
```

---

*Next document: Document 4 — The IETF Draft*
