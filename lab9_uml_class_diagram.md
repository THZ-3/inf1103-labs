# Week 11 Lab 9 – UML Class Diagram

`-` = private, `+` = public, `*` = abstract method, underlined / `$` = static method. Types are language-independent: `String`, `float`, `int`, `bool`, `void`; a collection is written as `Type [0..*]`.

![Lab 9 UML class diagram](lab9_uml_class_diagram.png)

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
        -__discount : DiscountStrategy
        +__init__(order_id : String, discount : DiscountStrategy | None)
        +get_order_id() String
        +get_discount() DiscountStrategy
        +set_discount(discount : DiscountStrategy) void
        +add_order_line(product : Product, quantity : int) void
        +remove_order_line(product_id : String) bool
        +get_order_lines() OrderLine [0..*]
        +calculate_subtotal() float
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

    class DiscountStrategy {
        <<abstract>>
        +apply(total : float)* float
    }

    class NoDiscount {
        +apply(total : float) float
    }

    class PercentageDiscount {
        -__percentage : float
        +__init__(percentage : float)
        +get_percentage() float
        +apply(total : float) float
    }

    class BulkDiscount {
        -__threshold : float
        -__amount : float
        +__init__(threshold : float, amount : float)
        +get_threshold() float
        +get_amount() float
        +apply(total : float) float
    }

    class StudentDiscount {
        +STUDENT_PERCENTAGE : float = 5
        +__init__()
    }

    class ProductFactory {
        +create(product_type : String, product_id : String, name : String, price : float, stock_quantity : int, supplier : Supplier, weight : float, download_size : float)$ Product
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Supplier "1" -- "0..*" Product : supplies
    Inventory "0..1" o-- "0..*" Product : contains
    Order "1" *-- "0..*" OrderLine : owns
    OrderLine "0..*" --> "1" Product : refers to
    DiscountStrategy <|-- NoDiscount
    DiscountStrategy <|-- PercentageDiscount
    DiscountStrategy <|-- BulkDiscount
    PercentageDiscount <|-- StudentDiscount
    Order "0..*" --> "1" DiscountStrategy : uses
    ProductFactory ..> Product : «creates»
```

## New in Lab 9

| Relationship | Notation | Multiplicity | Why |
|---|---|---|---|
| `NoDiscount`, `PercentageDiscount`, `BulkDiscount` → `DiscountStrategy` | Inheritance: solid line, hollow triangle at DiscountStrategy | – | Each **is a** DiscountStrategy and implements `apply()` |
| `StudentDiscount` → `PercentageDiscount` | Inheritance | – | A StudentDiscount **is a** 5% PercentageDiscount |
| `Order` → `DiscountStrategy` | **Association**: solid line with an arrow | Order 0..* — 1 DiscountStrategy | An Order **uses** exactly one strategy at a time to calculate its total. The strategy is not part of the Order, is created outside it, can be swapped with `set_discount()`, and one strategy object can be shared by many Orders |
| `ProductFactory` → `Product` | **Dependency**: dashed arrow labelled «creates» | – | The factory creates Products but does not store them |

## Relationships kept from Lab 8

| Relationship | Notation | Multiplicity |
|---|---|---|
| `PhysicalProduct`, `DigitalProduct` → `Product` | Inheritance | – |
| `PhysicalProduct` → `CanBeShipped` | Realisation: dashed line, hollow triangle | – |
| `Supplier` — `Product` | Association | Supplier 1 — 0..* Product |
| `Inventory` ◇— `Product` | Aggregation | Inventory 0..1 ◇— 0..* Product |
| `Order` ◆— `OrderLine` | Composition | Order 1 ◆— 0..* OrderLine |
| `OrderLine` → `Product` | Association | OrderLine 0..* — 1 Product |

## Notes

- `DiscountStrategy` is `<<abstract>>`: it only declares `apply()`. `Order` depends on this abstraction and never on a specific discount class, so a new discount is a new class with no change to `Order`.
- `ProductFactory.create()` is a static method that returns the abstract type `Product`. Only the factory knows the concrete classes `PhysicalProduct` and `DigitalProduct`.
- `__init__(order_id, discount : DiscountStrategy | None)`: when no strategy is given, the Order uses a `NoDiscount`, so it always holds exactly one strategy.
- File handling (`file_handler.py`, including `load_products()`), input helpers (`input_helpers.py`) and the menu (`oop_auditor.py`) are plain functions, not classes.
