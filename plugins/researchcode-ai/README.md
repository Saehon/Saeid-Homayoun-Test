# ResearchCode AI — Open research code & data specialist plugin

**Version 0.1.0 · MVP · Read-only public metadata · Python standard library**

A cross-platform research plugin for accounting, auditing, finance, economics and management, with **19 original workflow skills**, **7 read-only/analytical MCP tools**, one reviewer-engine and compatibility manifests for **ChatGPT / Codex**, **Claude Code / Cowork**, and **Gemini CLI**.

> **Current scope:** functional local MCP server; deterministic calculations; search and candidate identification (not confirmed replication). No code execution, no proprietary FT50/AJG list, no S&P Capital IQ entitlement, no redistribution of licensed datasets, no hosted MCP endpoint. UI/platform installations require their own checks.

## Capabilities

1. `search_publications` — public metadata via OpenAlex, rank filter only with verified local FT50/AJG registry.
2. `resolve_doi` — Crossref publisher metadata.
3. `find_replication` — Zenodo and Harvard Dataverse candidate dataset deposits; no false claim of verified association.
4. `classify_journal` — edition-specific ranking against validated registry.
5. `replication_checklist` — evidence passport and security checklist (never executes paper code).
6. `reconcile_balances` — GL and subledger arithmetic.
7. `variance_analysis` — actual vs budget/period arithmetic.

## Quick test (no external dependencies)

```bash
python3 -m unittest discover -s tests -v
printf '{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n' | python3 server.py
```

## Installation

### ChatGPT / Codex
`plugin.json`, `mcp.json` and `skills/` follow the portable Agent Plugins structure. Use Plugin Creator or a repo-local marketplace. ChatGPT web/cloud may require a separately registered **hosted MCP service**, not the local stdio server; this package does not pretend it is deployed. Add a custom registered service for cloud usage after separately hosting and securing one.

### Claude Code / Cowork
The `.claude-plugin/plugin.json`, `.mcp.json`, `commands/`, and `skills/` form a Claude-compatible plugin. In Claude Code, register a local marketplace that contains this folder, then install `researchcode-ai`; or connect the stdio MCP server directly. Keep Python 3.11+ available in the host environment. This does **not** install Anthropic Finance or Data plugins automatically; those are distinct optional official plugins.

### Gemini CLI
The repository includes `gemini-extension.json` and `GEMINI.md`. Install the folder or its GitHub repository as a Gemini CLI extension (`gemini extensions install PATH_OR_REPOSITORY_URL`). The same stdio MCP tools are used. Browser Gemini integration is not represented as already working.

### GitHub
Publish this repository, run GitHub Actions unit tests, provide a tagged source release and ensure no `.env`, `restricted_data/`, proprietary ranking snapshots or third-party data are committed. A repository and README is not itself a hosted SaaS endpoint or published ChatGPT directory listing.

## Journal ranking setup

The shipped `data/journal_registry.csv` is intentionally **empty except for headers** because FT50 and AJG editions and list rights must be verified. To enable filters, load an authorized ranking CSV with fields `journal,issn,ft50,ajg,ranking_edition,verification_status,source_url` and values `verification_status=verified` backed by an official URL and edition. For privacy or restricted rankings place the CSV **outside** the public repo and point `RESEARCHCODE_JOURNAL_CSV` to its absolute path. Never ship non-redistributable lists.

## OpenAlex usage
Anonymous casual API requests work, subject to provider quota. Set `OPENALEX_API_KEY` in your own environment for larger workloads; never include secrets in plugin JSON. Public API results are not guarantees of open materials.

## Boundaries

- Does not run any downloaded research code. No observed coefficients, regression results, studies or benchmark claims are fabricated.
- S&P Capital IQ/Kensho, WRDS, CRSP, Compustat, Audit Analytics, Bloomberg and Refinitiv require separate entitlement. This package includes **guidance skill** only for Capital IQ.
- Finance/audit outputs require qualified professional and human review. It cannot make regulatory opinions or post journal entries.
- No instrument-level Snowflake, Databricks, BigQuery, SAP, NetSuite or ERP connection exists until explicitly configured and authorized.
- Reviewer-engine performs traceability and falsification checklists, not autonomous FT50 acceptance grading.

## Next milestones

- Integrate DataCite relations, OpenICPSR/AEA deposits, automatic provenance confirmation with human review.
- Add read-only package manifest inspection and SHA256; secure, network-isolated containers for opt-in execution.
- Implement versioned journal importer and reviewer-approved ranking snapshot verification.
- Implement authenticated hosted MCP service with security, quota and OAuth for ChatGPT web use.
- Run independent protocol tests with installed Claude Code and Gemini CLI and the ChatGPT plugin submission flow.

See `docs/` for skill catalog, reviewer gates, citations, and a reusable master research prompt.

## Licensing
MIT for this original plugin code and skill instructions. Upstream public data remains governed by its own license. No private research data, Anthropic plugin source or S&P code is bundled.
