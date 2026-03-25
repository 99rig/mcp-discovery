# Document 2 — The Technical Proposal

## Defining mcp:// as a URI scheme

`mcp://` is a machine-to-machine URI scheme that identifies a publicly reachable MCP server on a web domain.

It is not intended for humans — it is not typed into a browser. It is used exclusively by AI agents and automated crawlers to discover and connect to MCP servers.

```
mcp://bolts.com          → MCP server on domain bolts.com
mcp://api.shop.it        → MCP server on subdomain
mcp://bolts.com/shop     → MCP server on specific path
```

---

## Formal ABNF grammar

An RFC requires the precise syntactic definition of the URI scheme in ABNF (Augmented Backus-Naur Form) format, as defined by RFC 5234:

```abnf
mcp-URI         = "mcp://" authority path-abempty [ "?" query ]
authority       = [ userinfo "@" ] host [ ":" port ]
host            = IP-literal / IPv4address / reg-name
reg-name        = *( unreserved / pct-encoded / sub-delims )
path-abempty    = *( "/" segment )
segment         = *pchar
query           = *( pchar / "/" / "?" )
userinfo        = *( unreserved / pct-encoded / sub-delims / ":" )
port            = *DIGIT
unreserved      = ALPHA / DIGIT / "-" / "." / "_" / "~"
pct-encoded     = "%" HEXDIG HEXDIG
sub-delims      = "!" / "$" / "&" / "'" / "(" / ")"
                / "*" / "+" / "," / ";" / "="
pchar           = unreserved / pct-encoded / sub-delims / ":" / "@"
; References: RFC 3986 (URI Generic Syntax), RFC 5234 (ABNF)
```

Valid examples:
```
mcp://bolts.com
mcp://api.bolts.com
mcp://bolts.com/shop
mcp://bolts.com:8080
mcp://bolts.com/catalog/fasteners
```

Invalid examples:
```
mcp://            (missing host)
mcp:bolts.com     (missing //)
mcp://bolts.com?  (empty query not allowed)
```

---

## How an mcp:// address is resolved

Resolution follows a well-defined cascade sequence. Clients MUST follow this order:

```
INPUT: mcp://bolts.com

STEP 1 — Discovery via .well-known (high priority)
  → Client performs:
    GET https://bolts.com/.well-known/mcp-server
    Accept: application/json
  → 200 OK with valid JSON → use the manifest
  → 301/302 → follow redirect (max 2 levels)
  → 404 or timeout → proceed to STEP 2

STEP 2 — Discovery via DNS TXT (fallback)
  → Client performs DNS query:
    _mcp.bolts.com  IN  TXT
  → Record present with v=mcp1 → extract endpoint
  → Absent → proceed to STEP 3

STEP 3 — Direct fallback (last resort)
  → Client attempts connection at:
    https://bolts.com/mcp
  → Valid MCP handshake → use endpoint
  → Fails → ERROR: no MCP server found

OUTPUT: MCP endpoint URL or error
```

Note: clients MUST prefer `.well-known` over DNS because HTTPS provides domain authenticity guarantees superior to unsigned DNS.

---

## The manifest /.well-known/mcp-server

The `/.well-known/mcp-server` endpoint returns a JSON document — the **manifest** — with the MCP server metadata. It is the equivalent of `robots.txt` for crawlers, but for AI agents.

### Required vs optional fields

| Field | Type | Requirement | Description |
|---|---|---|---|
| `mcp_version` | string | MUST | MCP spec version (e.g. `2025-06-18`) |
| `name` | string | MUST | Human-readable server name |
| `endpoint` | string (URL) | MUST | URL of the actual MCP endpoint |
| `transport` | string | MUST | `http` or `stdio` |
| `description` | string | SHOULD | Natural language description |
| `auth` | object/string | SHOULD | Authentication type required |
| `capabilities` | array | SHOULD | List of exposed primitives |
| `categories` | array | MAY | Semantic categories |
| `languages` | array | MAY | Supported languages (ISO 639-1) |
| `coverage` | string | MAY | Geographic coverage (ISO 3166-1) |
| `contact` | string | MAY | Contact email or URL |
| `docs` | string (URL) | MAY | Documentation URL |
| `last_updated` | string (ISO 8601) | MAY | Last update date |
| `crawl` | boolean | MAY | `false` to opt out of indexing |

### Minimal structure (MUST)

```json
{
  "mcp_version": "2025-06-18",
  "name": "Bolts.com MCP Server",
  "endpoint": "https://bolts.com/mcp",
  "transport": "http"
}
```

### Full structure (SHOULD + MAY)

```json
{
  "mcp_version": "2025-06-18",
  "name": "Bolts.com MCP Server",
  "description": "Catalog of bolts, screws and metal fasteners",
  "endpoint": "https://bolts.com/mcp",
  "transport": "http",
  "auth": {
    "type": "oauth2",
    "discovery": "https://bolts.com/.well-known/oauth-protected-resource"
  },
  "capabilities": ["tools", "resources", "prompts"],
  "categories": ["e-commerce", "hardware", "fasteners"],
  "languages": ["en", "it"],
  "coverage": "US",
  "last_updated": "2026-03-25T00:00:00Z",
  "contact": "api@bolts.com",
  "docs": "https://bolts.com/mcp/docs",
  "crawl": true
}
```

### Expected HTTP response

The server MUST respond with:
```
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=3600
```

---

## DNS TXT record (alternative to .well-known)

For operators who control DNS but not the web server:

```
_mcp.bolts.com  IN  TXT  "v=mcp1; endpoint=https://bolts.com/mcp; auth=none"
```

| Field | Requirement | Description |
|---|---|---|
| `v=mcp1` | MUST | Version discriminator |
| `endpoint=<url>` | MUST | MCP endpoint URL |
| `auth=<type>` | SHOULD | `none`, `apikey`, `oauth2` |

Analogy: same approach used by SPF (`v=spf1`) and DKIM for email.
Limitation: DNS TXT records are limited to 255 characters. For complete manifests, `.well-known` MUST be used.

---

## Relationship with existing RFCs

| RFC | Title | Use in this document |
|---|---|---|
| RFC 3986 | URI Generic Syntax | Base for `mcp://` ABNF syntax |
| RFC 8615 | Well-Known URIs | Base for `/.well-known/mcp-server` |
| RFC 8259 | JSON | Manifest format |
| RFC 1035 | DNS | `_mcp` TXT record |
| RFC 2119 | Key words in RFCs | MUST/SHOULD/MAY semantics |

---

*Next document: Document 3 — The Crawler*
