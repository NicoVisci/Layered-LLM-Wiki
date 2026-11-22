---
kind: scenario
module: sales
status: current
quality: reliability
actors: [../actors/shopper.md]
domain: [../domain/order.md, ../domain/payment.md]
use_cases: [../application/pay-for-an-order.md]
cites: [an-order-is-paid-exactly-once.md]
---

# Payment provider is not available

| Part | Value |
| --- | --- |
| Source | A shopper |
| Stimulus | Pays for an order |
| Environment | The payment provider does not answer |
| Response | The system keeps the order not paid and tells the shopper to try again |
| Response measure | No order is paid two times. The answer comes in less than 5 seconds. |
