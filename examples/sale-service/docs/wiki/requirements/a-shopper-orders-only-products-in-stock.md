---
kind: requirement
module: sales
status: current
actors: [../actors/shopper.md]
domain: [../domain/order.md, ../domain/product.md, ../domain/stock-never-goes-below-zero.md]
use_cases: [../application/place-an-order.md]
cites: []
---

# A shopper orders only products in stock

- **R1:** When a shopper orders a quantity that is more than the stock, the system shall
  refuse the order.
- **R2:** When the system accepts an order, the system shall decrease the stock of each
  product by the ordered quantity.
