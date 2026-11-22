---
kind: requirement
module: sales
status: current
actors: [../actors/shopper.md]
domain: [../domain/order.md, ../domain/payment.md, ../domain/an-order-is-paid-once.md]
use_cases: [../application/pay-for-an-order.md]
cites: []
---

# An order is paid exactly once

- **R1:** When the payment provider accepts a payment, the system shall mark the order
  as paid.
- **R2:** When a shopper pays for an order that is already paid, the system shall refuse
  the payment.
