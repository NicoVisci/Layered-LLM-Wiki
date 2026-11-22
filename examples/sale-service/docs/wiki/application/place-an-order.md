---
kind: use-case
module: sales
status: current
---

# Place an order

1. The shopper selects [products](../domain/product.md) and quantities.
2. The system reads the stock through [ProductCatalog](product-catalog.md).
3. The system makes an [order](../domain/order.md) and saves it through
   [OrderRepository](order-repository.md).
