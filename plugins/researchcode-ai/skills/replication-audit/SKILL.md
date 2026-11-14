---
name: replication-audit
description: Assess reproducibility of published empirical code and data
---

# Replication Audit

## Inputs
Paper DOI and version, repository DOI/URL, license, software environment, stated sample and original table expectations.

## Workflow
1. Call `replication_checklist`. Capture links and original release identifiers. Verify publisher-to-repository provenance using author name, dates and documented DOI relations.
2. Collect read-only SHA256 hashes, data dictionary, environment lockfile, commands, random seeds and dataset licenses. Inspect for credential exfiltration and destructive commands before allowing any later sandbox use.
3. Do not run untrusted scripts in the MCP server. Execution must happen in an isolated, network-blocked, resource-limited runner with pre-approved input data.
4. Compare coefficients, signs, N, standard errors and figures to the original article with explicitly declared tolerance.
5. Score states: `discovered`, `verified_package`, `runnable`, `replicated`, `partially_replicated`, `not_replicated`, `restricted`, `not_tested`. In v0.1.0 output `not_tested` unless independent evidence exists.
6. Disclose code/data availability separately. Reproducing a table does not prove causal identification, construct validity or conclusions.

## Output
A structured evidence passport with DOI, journal tier provenance, package, license, method, dataset restriction, checksums, runtime, differences and evaluator sign-off.
