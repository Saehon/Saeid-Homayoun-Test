---
name: reconciliation
description: Reconcile GL to bank, subledger and intercompany balances
---

# Reconciliation

## Inputs
Source periods and currencies, GL closing balance, bank/subledger balance, outstanding cheques, deposits in transit, cut-off and known adjustments.

## Procedure
Validate that amounts have the same currency, date and sign convention. Use `reconcile_balances` for deterministic arithmetic, then investigate and age reconciling items, duplicated or stale transactions and unsupported adjustments. Do not treat a zero arithmetic difference as evidence that accounts are accurate. Output traceable reconciling-item IDs, amounts, reasons, aging, proposed action and approval status. Never generate unapproved postings.
