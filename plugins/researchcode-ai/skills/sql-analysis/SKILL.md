---
name: sql-analysis
description: Write safe read-only SQL for linked research datasets
---

# Sql Analysis

## Procedure
Discover actual table schemas and key constraints before writing SQL. Start from the unit of analysis, population, inclusive/exclusive dates, primary key and data rights. Build parameterized SELECT queries with explicit joins and time alignment, limit preview rows, show null-handling and unit conversion. Prohibit INSERT/UPDATE/DELETE/DROP unless specifically authorized outside this plugin. State dialect and estimated query cost; never assert a query was executed unless connector returns results. Do not assume Snowflake, Databricks or BigQuery connection is available.
