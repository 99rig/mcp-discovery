# Document 4 — The IETF Draft

## What is an Internet Draft

An Internet Draft (I-D) is the working document that precedes an official RFC. It is public, open to comments, and anyone can publish one on datatracker.ietf.org.

The name follows the IETF convention:
```
draft-[authors]-mcp-discovery-uri-00
```

---

## Formal draft structure

An RFC has precisely defined mandatory sections:

```
1. Abstract          → summary of max 150 words
2. Introduction      → context, problem, motivation
3. Terminology       → precise definitions of every term
4. The mcp:// URI    → formal ABNF syntax, semantics, examples
5. MCP Discovery     → /.well-known, DNS TXT, resolution sequence
6. The Manifest      → JSON schema, fields, examples
7. Security          → spoofing, DNS hijacking, rate limiting
8. IANA              → registration of mcp:// and .well-known/mcp-server
9. References        → normative and informative
```

---

## RFC technical language (MUST/SHOULD/MAY)

Each RFC uses these terms with precise meaning, defined by RFC 2119:

| Term | Meaning |
|---|---|
| **MUST** | Absolute requirement — violation breaks interoperability |
| **MUST NOT** | Absolute prohibition |
| **SHOULD** | Recommended — exceptions allowed if justified |
| **SHOULD NOT** | Discouraged — exceptions allowed if justified |
| **MAY** | Optional — free implementation |

---

## Current status

### Published drafts

| Version | URL | Date |
|---|---|---|
| -00 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/00/ | 2026-03-25 |
| -01 | https://datatracker.ietf.org/doc/draft-serra-mcp-discovery-uri/01/ | 2026-03-25 |

Changes from -00 to -01:
- Added Section 1.3 "Relationship to Other Work" — explicitly acknowledges SEP-1649 and proposes coordination
- Added Section 7 "Reference Implementation" with live endpoint at mcpstandard.dev
- Updated Informative References: SEP-1649, MCPSTANDARD, GH-DISCUSSION
- Added author URI: https://mcpstandard.dev

### Communications

- Email sent to `dispatch@ietf.org` — 2026-03-25 ✅
- GitHub discussion #2462 opened and updated — 2026-03-25 ✅

### Domain and implementation

- **mcpstandard.dev** — project domain
- **https://mcpstandard.dev/.well-known/mcp-server** — live reference implementation
- **https://github.com/99rig/mcp-discovery** — GitHub repository

---

## Relationship with existing work

### SEP-1649

The MCP community has independently explored similar ideas. SEP-1649, authored by MCP specification maintainers (`@dsp-ant` and `@nickcoai` at Anthropic), proposes a `/.well-known/mcp.json` endpoint for server card discovery. That proposal explicitly notes the need to register the well-known suffix with IANA per RFC 8615.

This IETF draft addresses the same discovery problem from the internet standards track, defining a formal URI scheme (`mcp://`) and requesting the necessary IANA registrations. The authors welcome coordination with MCP maintainers to align the well-known path and manifest schema.

### Key difference

SEP-1649 focuses on discovery within an already-established MCP connection; this draft focuses on **pre-connection discovery** starting from a bare domain name — as required for autonomous agent operation and web-scale crawling.

---

## How to submit to the IETF community

```
STEP 1 — Publication
  datatracker.ietf.org/submit/
  Upload .txt file → Post submission

STEP 2 — Notification
  Email to dispatch@ietf.org
  Announce the draft and the problem it solves
  Include link to concrete implementation

STEP 3 — IETF Meeting (3 times per year)
  Present in Birds of a Feather (BoF) session
  A BoF evaluates whether there is interest in forming a Working Group

STEP 4 — Iteration
  Community comments, critiques, improves
  Publish -01, -02, ... until consensus

STEP 5 — Working Group
  If problem gains consensus → dedicated WG formed
  WG brings draft to official RFC
```

---

## Realistic timeline

```
Month 1-2   → draft -00 and -01 published        ✅ DONE
Month 3     → IETF and GitHub feedback            ← NOW
Month 4-6   → revisions -02, -03
Month 6-12  → IETF meeting, BoF
Year 1-3    → Working Group and RFC
```

The RFC is not the immediate goal. The immediate goal is **draft + implementation + sites using it**. The RFC ratifies what already works.

---

## The advantage of implementing first

You don't need to wait for the RFC to start. Publishing the draft + implementing the crawler + releasing the WordPress plugin creates the **fait accompli**:

```
"Here is the draft, here is the implementation, here are 500 sites already using it.
Let's standardize what already works."
```

This is exactly the story of HTTP, OAuth, JSON, and dozens of other standards born this way.
