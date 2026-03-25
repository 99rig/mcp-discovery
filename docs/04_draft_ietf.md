# Documento 4 — Il Draft IETF

## Cos'è un Internet Draft

Un Internet Draft (I-D) è il documento di lavoro che precede una RFC ufficiale. È pubblico, aperto a commenti, e chiunque può pubblicarne uno su datatracker.ietf.org.

```
draft-[autori]-mcp-discovery-uri-00
```

---

## Struttura formale

```
1. Abstract          → sintesi di max 150 parole
2. Introduction      → contesto, problema, motivazione
3. Terminology       → definizioni precise
4. The mcp:// URI    → sintassi ABNF, semantica, esempi
5. MCP Discovery     → /.well-known, DNS TXT, sequenza
6. The Manifest      → schema JSON, campi, esempi
7. Security          → spoofing, DNS hijacking, rate limiting
8. IANA              → registrazione mcp:// e .well-known/mcp-server
9. References        → normative e informative
```

---

## Linguaggio tecnico RFC

| Termine | Significato |
|---|---|
| **MUST** | Obbligo assoluto |
| **MUST NOT** | Divieto assoluto |
| **SHOULD** | Raccomandato — eccezioni ammesse se motivate |
| **SHOULD NOT** | Sconsigliato — eccezioni ammesse se motivate |
| **MAY** | Opzionale |

---

## Stato attuale

### Draft pubblicati

| Versione | URL | Data |
|---|---|---|
| -00 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/00/ | 2026-03-25 |
| -01 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/01/ | 2026-03-25 |

Modifiche da -00 a -01:
- Aggiunta sezione 1.3 "Relationship to Other Work" — cita SEP-1649
- Aggiunta sezione 7 "Reference Implementation" con live endpoint
- Aggiornate Informative References: SEP-1649, MCPSTANDARD, GH-DISCUSSION
- Aggiunto URI autore: https://mcpstandard.dev

### Comunicazioni

- Email inviata a `dispatch@ietf.org` — 2026-03-25
- Discussion GitHub #2462 aperta: https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/2462

### Dominio e implementazione

- **mcpstandard.dev** — dominio del progetto
- **https://mcpstandard.dev/.well-known/mcp-server** — reference implementation live
- **https://github.com/99rig/mcp-discovery** — repository GitHub

---

## Come presentarlo alla community IETF

```
PASSO 1 — Pubblicazione
  datatracker.ietf.org/submit/ → Upload .txt → Post submission

PASSO 2 — Notifica
  Email a dispatch@ietf.org con link al draft e all'implementazione

PASSO 3 — IETF Meeting (3 volte l'anno)
  Presenta in sessione Birds of a Feather (BoF)

PASSO 4 — Iterazione
  -01, -02, ... fino al consensus

PASSO 5 — Working Group
  Se ottiene trazione → WG dedicato → RFC ufficiale
```

---

## Timeline realistica

```
Mese 1-2   → draft -00 e -01 pubblicati        ✅ FATTO
Mese 3     → feedback IETF e GitHub             ← ADESSO
Mese 4-6   → revisioni -02, -03
Mese 6-12  → IETF meeting, BoF
Anno 1-3   → Working Group e RFC
```

La RFC non è l'obiettivo immediato. Il fatto compiuto è: **draft + implementazione + siti che lo usano**.
