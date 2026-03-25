# Documento 2 — La Proposta Tecnica

## Definizione di mcp:// come URI scheme

`mcp://` è uno URI scheme machine-to-machine che identifica un server MCP raggiungibile pubblicamente su un dominio web. Non è pensato per gli umani — è usato esclusivamente da agenti AI e crawler automatici.

```
mcp://viti.com          → server MCP sul dominio viti.com
mcp://api.negozio.it    → server MCP su sottodominio
mcp://viti.com/shop     → server MCP su path specifico
```

---

## Grammatica ABNF formale

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
; Riferimenti: RFC 3986 (URI Generic Syntax), RFC 5234 (ABNF)
```

---

## Come si risolve un indirizzo mcp://

```
INPUT: mcp://viti.com

STEP 1 — Discovery via .well-known (priorità alta)
  GET https://viti.com/.well-known/mcp-server
  Accept: application/json
  → 200 OK + JSON valido → usa il manifest
  → 301/302 → segue redirect (max 2 livelli)
  → 404 o timeout → STEP 2

STEP 2 — Discovery via DNS TXT (fallback)
  _mcp.viti.com  IN  TXT
  → record con v=mcp1 → estrae endpoint
  → assente → STEP 3

STEP 3 — Fallback diretto (last resort)
  https://viti.com/mcp
  → handshake MCP valido → usa endpoint
  → fallisce → ERRORE: nessun server MCP trovato
```

---

## Il manifest /.well-known/mcp-server

| Campo | Tipo | Obbligo | Descrizione |
|---|---|---|---|
| `mcp_version` | string | MUST | Versione della spec MCP (es. `2025-06-18`) |
| `name` | string | MUST | Nome leggibile del server |
| `endpoint` | string | MUST | URL dell'endpoint MCP |
| `transport` | string | MUST | `http` oppure `stdio` |
| `description` | string | SHOULD | Descrizione in linguaggio naturale |
| `auth` | object | SHOULD | Tipo di autenticazione richiesta |
| `capabilities` | array | SHOULD | Lista di primitive esposte |
| `categories` | array | MAY | Categorie semantiche |
| `languages` | array | MAY | Lingue supportate (ISO 639-1) |
| `coverage` | string | MAY | Copertura geografica (ISO 3166-1) |
| `contact` | string | MAY | Email o URL di contatto |
| `docs` | string | MAY | URL documentazione |
| `last_updated` | string | MAY | Data ultimo aggiornamento (ISO 8601) |
| `crawl` | boolean | MAY | `false` per opt-out indicizzazione |

### Struttura minima

```json
{
  "mcp_version": "2025-06-18",
  "name": "Viti.com MCP Server",
  "endpoint": "https://viti.com/mcp",
  "transport": "http"
}
```

### Struttura completa

```json
{
  "mcp_version": "2025-06-18",
  "name": "Viti.com MCP Server",
  "description": "Catalogo viti, bulloni e minuteria metallica",
  "endpoint": "https://viti.com/mcp",
  "transport": "http",
  "auth": { "type": "oauth2", "discovery": "https://viti.com/.well-known/oauth-protected-resource" },
  "capabilities": ["tools", "resources", "prompts"],
  "categories": ["e-commerce", "hardware", "fasteners"],
  "languages": ["it", "en"],
  "coverage": "IT",
  "last_updated": "2026-03-25T00:00:00Z",
  "contact": "api@viti.com",
  "docs": "https://viti.com/mcp/docs",
  "crawl": true
}
```

---

## Record DNS TXT (alternativa a .well-known)

```
_mcp.viti.com  IN  TXT  "v=mcp1; endpoint=https://viti.com/mcp; auth=none"
```

| Campo | Obbligo | Descrizione |
|---|---|---|
| `v=mcp1` | MUST | Versione del record |
| `endpoint=<url>` | MUST | URL dell'endpoint MCP |
| `auth=<tipo>` | SHOULD | `none`, `apikey`, `oauth2` |

Limitazione: max 255 caratteri. Per manifest complessi usare `.well-known`.

---

## Relazione con le RFC esistenti

| RFC | Titolo | Uso |
|---|---|---|
| RFC 3986 | URI Generic Syntax | Base per la sintassi ABNF di `mcp://` |
| RFC 8615 | Well-Known URIs | Base per `/.well-known/mcp-server` |
| RFC 8259 | JSON | Formato del manifest |
| RFC 1035 | DNS | Record TXT `_mcp` |
| RFC 2119 | Key words in RFCs | Semantica di MUST/SHOULD/MAY |

---

*Prossimo documento: Documento 3 — Il Crawler*
