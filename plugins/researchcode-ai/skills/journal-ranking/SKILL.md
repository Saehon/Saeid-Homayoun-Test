---
name: journal-ranking
description: Verify FT50 and AJG 3/4/4-star journal classification by edition
---

# Journal Ranking

## Rule
FT50, AJG 4-star, AJG 4 and AJG 3 are journal-list indicators, never grades assigned by an LLM. Do not infer list membership from prestige, journal name or citations.

## Procedure
Load a legally obtained or openly shareable ranking snapshot into `data/journal_registry.csv` or an external `RESEARCHCODE_JOURNAL_CSV`. Required columns: journal, issn, ft50, ajg, ranking_edition, verification_status, source_url. Only set `verification_status=verified` after checking source, journal identity, ranking edition and licence. Retain older editions rather than overwriting history; when comparing time windows state the reference edition. The MCP tool returns `unverified` without these fields.

Use `FT50` for confirmed Financial Times list membership; AJG rating values are `3`, `4` or `4*`. Never substitute Scimago quartiles or JCR impact factors for AJG grades.
