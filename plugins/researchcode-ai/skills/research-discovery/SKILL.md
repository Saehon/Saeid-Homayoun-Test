---
name: research-discovery
description: Discover papers with public code or data and verifiable links
---

# Research Discovery

## Workflow
1. Clarify research construct, journal tier, time window, discipline and geographic setting from the request.
2. Call `search_publications` for candidate papers and `resolve_doi` for publisher metadata; maintain exact DOI and source URLs.
3. For selected DOIs call `find_replication`; categorize every hit as **unverified candidate** until its authors, title, DOI relations and package contents agree.
4. For FT50 or AJG/ABS tiers use `classify_journal`; if unverified, do not label it FT50/AJG or silently omit the uncertainty.
5. Report open access to the article, public code and public data as three separate dimensions. An openly available article is not necessarily open data.
6. Export a research matrix: DOI, title, year, journal, ranking edition, license, package URL, source URL, confidence and missingness. Never invent paper titles or article-to-code associations.

## Research priorities
Accounting, audit, finance, economics, management, information systems. Prefer direct archives, DOI-based deposit links, author pages, official repositories and documented versions. Flag potential selection bias in studies with posted code.
