---
kind: decision
module: sales
status: current
date: 2026-11-22
application: [../application/place-an-order.md, ../application/pay-for-an-order.md]
adapters: [../adapters/order-controller.md]
drivers: [../drivers/spring-web.md]
cites: []
---

# ADR-003: HTTP endpoint for orders

## Context

The shop front end must place and pay for orders.

## Decision

Expose the two use cases through one HTTP endpoint with Spring Web.

## Consequences

The use cases do not know HTTP.

## Alternatives considered

- A message queue. Rejected: the shopper waits for the answer.
