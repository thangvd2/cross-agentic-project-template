---
tags: [concept, financial-ledger]
products: [vault-core]
sources:
  - raw/vault-core-overview/vault_core_overview_what_is_vault_core.md
last_updated: 2026-04-21
---

# Postings

Postings are the fundamental mechanism for moving funds within Vault Core. A single posting represents an individual credit or debit of a specified amount. Vault Core adheres strictly to double-entry bookkeeping, meaning all fund movements must consist of a balanced set of credits and debits, encapsulated within a **Posting Instruction**.

## Posting Instruction Batches

Posting Instructions are grouped into **Posting Instruction Batches**, which serve as the atomic unit of acceptance or rejection. If a single instruction within a batch is rejected (e.g., due to insufficient funds or violating a smart contract rule), the entire batch is rejected.

> **TIP**: Posting batches should only group instructions that require atomic execution (e.g., a transaction and its associated fee). Bulk payments should be de-bulked into individual instructions rather than batched together.

## Accounts and Balances

Postings move funds between balance dimensions of accounts. Vault Core distinguishes between two types of accounts:
- **Customer Accounts**: Maintain associated [[concept-smart-contracts]] to enforce business logic and validate postings.
- **Internal Accounts**: Used for double-entry bookkeeping (e.g., a suspense or vostro account) but cannot contain smart contract logic.

### Balance Dimensions
Account balances are multi-dimensional and defined by four key coordinates:
1. **Asset Classes**: Designates the type of asset, such as Commercial Bank Money, Cash, or custom assets like reward points.
2. **Denominations**: Typically ISO currency codes, enabling multi-currency accounts natively.
3. **Addresses**: Segregates funds within a single account (e.g., `DEFAULT` for main balance, `FEES` for accrued charges, `SAVINGS` for rounding pots).
4. **Phases**: Indicates the availability of funds (`Committed`, `Pending Incoming`, `Pending Outgoing`).

## Posting Types

Postings move funds between account balance addresses of the same dimensions. Vault Core uses Posting Types to provide financial context to these movements. For example, Outbound Hard Settlement moves funds out of an account, while Inbound Hard Settlement moves funds in.

## Payment Devices

Vault Core uses **Payment Devices** to associate physical or virtual identifiers with a customer account. This allows various routing mechanisms (e.g., a physical card, an IBAN, or a sort code and account number) to direct postings to the correct underlying account.

## See Also
- [[entity-vault-core]]: The overarching core banking system.
- [[concept-financial-model]]: How postings construct the financial state and End of Day (EOD) processing.
- [[concept-smart-contracts]]: How smart contracts evaluate and process incoming postings.
