---
kind: use-case
module: sales
status: current
---

# Pay for an order

1. The shopper pays for an [order](../domain/order.md).
2. The system sends the [payment](../domain/payment.md) through
   [PaymentGateway](payment-gateway.md).
3. The system marks the order as paid through [OrderRepository](order-repository.md).
