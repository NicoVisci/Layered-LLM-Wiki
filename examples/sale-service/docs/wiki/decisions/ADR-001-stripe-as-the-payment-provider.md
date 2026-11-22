---
kind: decision
module: sales
status: current
date: 2026-11-22
application: [../application/payment-gateway.md, ../application/pay-for-an-order.md]
adapters: [../adapters/stripe-payment-gateway.md]
drivers: [../drivers/stripe.md]
cites: [../requirements/an-order-is-paid-exactly-once.md, ../requirements/payment-provider-is-not-available.md]
---

# ADR-001: Stripe as the payment provider

## Context

The system must take card payments and must not take one payment two times.

## Decision

Use Stripe. StripePaymentGateway implements PaymentGateway and sends an idempotency key
with each payment.

## Consequences

A change of provider changes only the adapter.

## Alternatives considered

- A payment service of our own. Rejected: card data needs a certified provider.
