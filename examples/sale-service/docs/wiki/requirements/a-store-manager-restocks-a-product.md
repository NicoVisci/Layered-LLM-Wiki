---
kind: requirement
module: sales
status: current
actors: [../actors/store-manager.md]
domain: [../domain/product.md, ../domain/stock-never-goes-below-zero.md]
use_cases: [../application/restock-a-product.md]
cites: []
---

# A store manager restocks a product

- **R1:** When a store manager adds a quantity to a product, the system shall increase
  the stock by that quantity.
- **R2:** When the quantity is zero or less, the system shall refuse the change.
