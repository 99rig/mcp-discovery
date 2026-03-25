# Documento 3 — Il Crawler

## Cos'è il crawler MCP

Il crawler MCP è un sistema automatico che scansiona il web alla ricerca di server MCP esposti, li indicizza, e rende le loro capabilities interrogabili da agenti AI. È l'equivalente di Googlebot — ma invece di indicizzare pagine HTML per gli umani, indicizza endpoint MCP per le macchine.

---

## Come trova i siti con endpoint MCP

```
FONTE 1 — Scansione /.well-known
  Lista di domini noti (Alexa top 1M, Common Crawl)
  GET https://dominio/.well-known/mcp-server → se JSON valido → indicizza

FONTE 2 — Record DNS TXT
  Query DNS: _mcp.dominio → se v=mcp1 → indicizza

FONTE 3 — Registry esistenti
  Importa da registry.modelcontextprotocol.io, mcp.so, GitHub registry
  Verifica che gli endpoint siano ancora attivi

FONTE 4 — Segnalazione volontaria
  API pubblica per registrare mcp://miodominio.com
  Verifica ownership via DNS challenge o HTTP challenge
  Analogo a Google Search Console

FONTE 5 — Link nel web
  Scansiona pagine HTML cercando:
  <link rel="mcp-server" href="/.well-known/mcp-server">
```

---

## Come indicizza le capabilities

```
FASE 1 — Lettura manifest
  GET /.well-known/mcp-server → estrae name, description, endpoint, categories

FASE 2 — Connessione MCP
  POST endpoint/mcp (handshake initialize)
  tools/list → lista tools con nome, descrizione, schema JSON
  resources/list → lista risorse disponibili
  prompts/list → lista prompt templates

FASE 3 — Indicizzazione semantica
  Genera embedding vettoriale per ogni tool
  Salva in pgvector per ricerca semantica

FASE 4 — Categorizzazione
  Assegna categorie: e-commerce, finanza, salute, legal, logistics,
  knowledge-base, dev-tools, media, travel, ...

FASE 5 — Aggiornamento periodico
  Ping ogni 24h per verificare attività
  Re-indicizza se last_updated cambia
  Rimuove dall'indice dopo 7 giorni di inattività
```

---

## La Search API — specifica completa

### Endpoint

```
GET /v1/search
```

### Parametri

| Parametro | Tipo | Obbligo | Descrizione |
|---|---|---|---|
| `q` | string | MUST | Query in linguaggio naturale o keywords |
| `category` | string | MAY | Filtro categoria (es. `e-commerce`) |
| `country` | string | MAY | Filtro geografico (ISO 3166-1) |
| `language` | string | MAY | Filtro lingua (ISO 639-1) |
| `auth` | string | MAY | `none`, `apikey`, `oauth2` |
| `limit` | integer | MAY | Risultati (default: 10, max: 50) |
| `offset` | integer | MAY | Paginazione (default: 0) |

### Esempio risposta

```json
{
  "query": "viti bulloni minuteria",
  "total": 12,
  "results": [
    {
      "mcp_uri": "mcp://viti.com",
      "name": "Viti.com MCP Server",
      "endpoint": "https://viti.com/mcp",
      "tools": [
        { "name": "search_products", "description": "Cerca prodotti per tipo e materiale" },
        { "name": "check_stock", "description": "Verifica disponibilità a magazzino" },
        { "name": "get_price", "description": "Ottieni prezzi aggiornati" }
      ],
      "relevance_score": 0.97,
      "last_verified": "2026-03-25T08:00:00Z"
    }
  ]
}
```

---

## Algoritmo di ranking

**1. Rilevanza semantica (peso 60%)** — distanza coseno tra embedding query e tools

**2. Qualità del server (peso 25%)** — uptime, tempo di risposta, completezza manifest

**3. Segnali contestuali (peso 15%)** — match geografico, linguistico, recency

---

## Analogia con Googlebot

| Googlebot | Crawler MCP |
|---|---|
| Scansiona URL HTTP | Scansiona domini per `/.well-known/mcp-server` |
| Indicizza testo HTML | Indicizza tools e capabilities MCP |
| SERP per umani | Search API per agenti AI |
| `robots.txt` | Campo `"crawl": false` nel manifest |

---

## Rate limiting etico

```
- Max 1 richiesta ogni 10 secondi per dominio
- Rispetta HTTP 429 con backoff esponenziale
- User-Agent: MCPCrawler/1.0
- Solo tools/list, resources/list, prompts/list — mai tools/call
```

---

## Stack tecnico

```
Crawler:   Python + asyncio, aiohttp, dnspython
Storage:   PostgreSQL + pgvector + Redis
API:       FastAPI + sentence-transformers + uvicorn
Infra:     cron job 24h + worker pool + Kubernetes
```

---

*Prossimo documento: Documento 4 — Il Draft IETF*
