# Week 10 Lab 8 – UML Class Diagram

`-` = private, `+` = public, `*` = abstract method. Types are language-independent: `String`, `float`, `int`, `bool`, `void`; a collection is written as `Type [0..*]`.

![Lab 8 UML class diagram](lab8_uml_class_diagram.png)

Mermaid source (renders on GitHub):

```mermaid
classDiagram
    class Supplier {
        -__supplier_id : String
        -__name : String
        -__contact_email : String
        +__init__(supplier_id : String, name : String, contact_email : String)
        +get_supplier_id() String
        +get_name() String
        +get_contact_email() String
        +display_information() void
        +to_dict() Dictionary
    }

    class Product {
        <<abstract>>
        -__product_id : String
        -__name : String
        -__price : float
        -__stock : int
        -__supplier : Supplier
        +__init__(product_id : String, name : String, price : float, stock : int, supplier : Supplier)
        +get_product_id() String
        +get_name() String
        +get_price() float
        +get_stock() int
        +get_supplier() Supplier
        +get_supplier_id() String
        +get_supplier_name() String
        +update_stock(quantity : int) bool
        +display_information() void
        +get_fulfilment_info()* String
        +to_dict() Dictionary
    }

    class PhysicalProduct {
        +BASE_SHIPPING_FEE : float = 5.00
        +SHIPPING_RATE_PER_KG : float = 2.00
        -__weight : float
        +__init__(product_id : String, name : String, price : float, stock : int, supplier : Supplier, weight : float)
        +get_weight() float
        +display_information() void
        +get_fulfilment_info() String
        +to_dict() Dictionary
        +calculate_shipping_cost() float
    }

    class DigitalProduct {
        -__download_size : float
        +__init__(product_id : String, name : String, price : float, stock : int, supplier : Supplier, download_size : float)
        +get_download_size() float
        +display_information() void
        +get_fulfilment_info() String
        +to_dict() Dictionary
    }

    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }

    class Inventory {
        -__products : Product [0..*]
        +__init__()
        +add_product(product : Product) bool
        +find_product(product_id : String) Product | None
        +remove_product(product_id : String) Product | None
        +update_stock(product_id : String, quantity : int) bool
        +display_all() void
        +get_products() Product [0..*]
    }

    class Order {
        -__order_id : String
        -__order_lines : OrderLine [0..*]
        +__init__(order_id : String)
        +get_order_id() String
        +add_order_line(product : Product, quantity : int) void
        +remove_order_line(product_id : String) bool
        +get_order_lines() OrderLine [0..*]
        +calculate_total() float
        +display_information() void
    }

    class OrderLine {
        -__product : Product
        -__quantity : int
        +__init__(product : Product, quantity : int)
        +get_product() Product
        +get_quantity() int
        +calculate_subtotal() float
        +display_information() void
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Supplier "1" -- "0..*" Product : supplies
    Inventory "0..1" o-- "0..*" Product : contains
    Order "1" *-- "0..*" OrderLine : owns
    OrderLine "0..*" --> "1" Product : refers to
```

## Relationships

| Relationship | Notation | Multiplicity | Why |
|---|---|---|---|
| `PhysicalProduct`, `DigitalProduct` → `Product` | Inheritance: solid line, hollow triangle at Product | – | Each **is a** Product |
| `PhysicalProduct` → `CanBeShipped` | Realisation: dashed line, hollow triangle at CanBeShipped | – | A PhysicalProduct **can be** shipped |
| `Supplier` — `Product` | **Association**: plain solid line | Supplier 1 — 0..* Product | Each product has one supplier; a supplier supplies any number. Neither owns the other, and both exist independently |
| `Inventory` ◇— `Product` | **Aggregation**: hollow diamond at Inventory | Inventory 0..1 ◇— 0..* Product | An Inventory is made of Products, but a Product can exist outside any Inventory and be moved between them |
| `Order` ◆— `OrderLine` | **Composition**: filled diamond at Order | Order 1 ◆— 0..* OrderLine | The Order creates its OrderLines; each line belongs to exactly one Order and never moves |
| `OrderLine` → `Product` | **Association**: solid line | OrderLine 0..* — 1 Product | A line refers to one Product but does not own it; the Product may also be in an Inventory |

## Notes

- `Product` is `<<abstract>>` and cannot be created directly. `get_fulfilment_info()` is abstract and implemented by both subclasses.
- `__supplier : Supplier` is a stored reference, but it is an **association**, not aggregation or composition: a Product is not a whole made of a Supplier.
- `Inventory` and `Order` type their collections by `Product` and `OrderLine`, so any Product subclass works without changes.
- `Product | None` means the method returns a Product, or nothing if no match is found.
- File handling (`file_handler.py`) and the menu (`oop_auditor.py`) are plain functions, not classes.
