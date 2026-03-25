# Documento 1 — Il Problema

## Background: cos'è MCP

Il Model Context Protocol (MCP) è un protocollo aperto pubblicato da Anthropic nel novembre 2024. Definisce un'interfaccia standard JSON-RPC 2.0 che permette agli agenti AI di connettersi a strumenti e servizi esterni — detti "server MCP" — per leggere dati, eseguire azioni, e interrogare risorse strutturate.

Un server MCP espone tre tipi di primitive:
- **Tools** — funzioni eseguibili dall'agente (es. `search_products`, `send_email`)
- **Resources** — dati leggibili come contesto (es. documenti, cataloghi, database)
- **Prompts** — template riutilizzabili per workflow standardizzati

MCP è già adottato da Claude (Anthropic), GitHub Copilot, Cursor, VS Code, e decine di altri client AI. Il numero di server MCP pubblici supera le migliaia e cresce rapidamente.

---

## Stato attuale della discovery MCP

Nonostante la crescita rapida dell'ecosistema, non esiste alcun meccanismo standard che permetta a un agente AI di **scoprire autonomamente** quali siti web o servizi espongono un server MCP.

L'unico modo attuale per connettere un agente AI a un server MCP è la **configurazione manuale**: qualcuno deve sapere che il server esiste, conoscere il suo URL, e configurarlo esplicitamente nel client AI. Questo crea una dipendenza strutturale dalla conoscenza umana che impedisce l'automazione autonoma.

---

## Perché i registry manuali non bastano

Esistono directory come `registry.modelcontextprotocol.io`, `mcp.so`, e il registry GitHub. Tuttavia presentano limiti strutturali:

- Richiedono **iscrizione volontaria** da parte del gestore del server — chi non sa che esistono non si iscrive
- Sono **aggiornati manualmente** e quindi per definizione incompleti e potenzialmente obsoleti
- Non esiste un meccanismo per verificare automaticamente che i server iscritti siano ancora attivi
- Funzionano come le Yellow Pages: ci si iscrive e si spera di essere trovati
- Un agente AI non li consulta automaticamente — dipende dalla configurazione del client
- Non coprono il **long tail** — migliaia di server piccoli e verticali che non si iscrivono mai

Il problema fondamentale è che i registry richiedono un'azione attiva da parte del gestore del server. Un meccanismo di discovery robusto deve funzionare anche senza questa azione.

---

## Perché il web search non basta

Un agente AI può usare strumenti di web search (Google, Bing, Brave) per trovare informazioni. Ma il web search è progettato per gli umani, non per gli agenti:

- I motori di ricerca indicizzano **testo HTML**, non endpoint MCP
- Non esiste un segnale semantico nel web che dica "questo sito espone un server MCP"
- Anche trovando un sito rilevante, l'agente non sa se espone MCP, su quale path, con quale autenticazione
- Il risultato è testo non strutturato da interpretare, non un endpoint interrogabile direttamente
- La latenza di una query web search è incompatibile con la discovery in tempo reale

---

## Il gap che esiste oggi

```
UMANO cerca "viti M6 inox dove comprare"
  → Google indicizza i siti
  → trova viti.com
  → pagina HTML con prezzi e catalogo

AGENTE AI cerca "viti M6 inox dove comprare"
  → web search → trova viti.com → legge HTML → interpreta testo
  → NON SA che viti.com ha un server MCP con catalogo strutturato
  → NON PUÒ interrogare direttamente stock, prezzi, disponibilità in tempo reale
  → risponde con informazioni approssimate estratte da testo
```

Il gap è preciso: **non esiste un protocollo che permetta a un agente AI di scoprire automaticamente un server MCP a partire da un dominio web**, né un'infrastruttura che indicizzi tali server in modo interrogabile.

Tre elementi mancano simultaneamente:
1. Uno **URI scheme** standard per identificare server MCP (`mcp://`)
2. Una **convenzione di discovery** per esporre i metadati del server (`/.well-known/mcp-server`)
3. Un **crawler** che indicizzi automaticamente gli endpoint MCP esposti

---

## A chi interessa risolverlo

**Lato offerta — chi espone server MCP**
- Gestori di siti e-commerce (WooCommerce, Shopify) → vogliono essere trovati dagli agenti AI
- Fornitori di API e dati strutturati → vogliono che i loro servizi siano interrogabili da agenti
- Aziende con knowledge base interne → vogliono esporre dati ai propri agenti AI

**Lato domanda — chi usa server MCP**
- Sviluppatori di agenti AI → vogliono poter interrogare servizi senza configurazione manuale
- Piattaforme AI (Anthropic, OpenAI, Google, Microsoft) → vogliono un ecosistema di tool discovery aperto
- Utenti finali → vogliono agenti AI che trovino autonomamente le risorse necessarie

**Lato standard**
- IETF e W3C → interesse a standardizzare prima che emergano soluzioni proprietarie incompatibili

---

## Requisiti di una soluzione

**R1 — Decentralizzazione**: Chiunque deve poter esporre un server MCP senza dipendere da un registry di terze parti.

**R2 — Scoperta automatica**: Un agente AI deve poter scoprire un server MCP a partire solo dal dominio web.

**R3 — Verificabilità**: L'agente deve poter verificare che il server MCP appartenga effettivamente al dominio indicato.

**R4 — Opt-out esplicito**: I gestori devono poter indicare di non voler essere indicizzati.

**R5 — Compatibilità con l'infrastruttura esistente**: DNS, HTTPS, `.well-known` — nessuna nuova infrastruttura.

**R6 — Semplicità di implementazione**: Idealmente un singolo file JSON statico.

---

## Non-obiettivi

- Il protocollo MCP in sé — già definito dalla specifica Anthropic
- L'autenticazione tra agente e server MCP — già coperta da OAuth 2.1
- Il formato dei tools, resources e prompts — già definito nella spec MCP
- La sicurezza delle operazioni eseguite tramite MCP — responsabilità del server
- La discovery di server MCP su reti private o intranet aziendali

---

## Analogia storica

Prima dei motori di ricerca, i siti web esistevano ma erano invisibili. Google ha risolto il problema con:
1. Un protocollo standard (HTTP) che tutti i siti già usavano
2. Un crawler che seguiva i link automaticamente
3. Un indice interrogabile

`mcp://` + `/.well-known/mcp-server` + un crawler MCP è la stessa architettura applicata all'ecosistema degli agenti AI. Il momento storico è analogo al 1993.

---

*Prossimo documento: Documento 2 — La Proposta Tecnica*
