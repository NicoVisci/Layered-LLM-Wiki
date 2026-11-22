---
kind: decision
module: sales
status: current
date: 2026-11-22
application: [../application/order-repository.md, ../application/product-catalog.md]
adapters: [../adapters/postgres-order-repository.md, ../adapters/postgres-product-catalog.md]
drivers: [../drivers/postgresql.md]
cites: [../requirements/a-shopper-orders-only-products-in-stock.md]
---

# ADR-002: PostgreSQL as the store

## Context

The stock change and the new order must occur together, or not at all.

## Decision

Use PostgreSQL. One transaction saves the order and decreases the stock.

## Consequences

The two adapters share one database.

## Alternatives considered

- A document database. Rejected: a change of two records needs a transaction.
