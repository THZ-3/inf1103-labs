# Week 9 Lab 7 – UML Class Diagram

`-` = private, `+` = public, *italic* / `*` = abstract method

```mermaid
classDiagram
    class Product {
        <<abstract>>
        -__product_id : String
        -__name : String
        -__price : float
        -__stock : int
        +__init__(product_id : String, name : String, price : float, stock : int)
        +get_product_id() String
        +get_name() String
        +get_price() float
        +get_stock() int
        +update_stock(quantity : int) bool
        +display_information() void
        +get_fulfilment_info()* String
        +to_dict() dict
    }

    class PhysicalProduct {
        -__weight : float
        +BASE_SHIPPING_FEE : float = 5.00
        +SHIPPING_RATE_PER_KG : float = 2.00
        +__init__(product_id : String, name : String, price : float, stock : int, weight : float)
        +get_weight() float
        +display_information() void
        +get_fulfilment_info() String
        +to_dict() dict
        +calculate_shipping_cost() float
    }

    class DigitalProduct {
        -__download_size : float
        +__init__(product_id : String, name : String, price : float, stock : int, download_size : float)
        +get_download_size() float
        +display_information() void
        +get_fulfilment_info() String
        +to_dict() dict
    }

    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }

    class Inventory {
        -__products : list~Product~
        +__init__()
        +add_product(product : Product) bool
        +search_product(product_id : String) Product
        +update_stock(product_id : String, quantity : int) bool
        +display_all() void
        +get_products() list~Product~
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Inventory "1" o-- "0..*" Product : contains
```

## Relationships

| Line | Meaning |
|---|---|
| `PhysicalProduct` → `Product`, solid line, hollow triangle | Inheritance: a PhysicalProduct **is a** Product |
| `DigitalProduct` → `Product`, solid line, hollow triangle | Inheritance: a DigitalProduct **is a** Product |
| `PhysicalProduct` → `CanBeShipped`, dashed line, hollow triangle | Interface realisation: a PhysicalProduct **can be** shipped |
| `Inventory` ◇— `Product`, 1 to 0..* | Aggregation: an Inventory holds any number of Products |

## Notes

- `Product` is `<<abstract>>`: it cannot be created directly, and every subclass must implement the abstract method `get_fulfilment_info()`.
- `CanBeShipped` is an `<<interface>>` (an abstract base class with only an abstract method and no attributes). Only `PhysicalProduct` implements it; `DigitalProduct` does not.
- `display_information()`, `get_fulfilment_info()` and `to_dict()` appear again in the subclasses because they **override** the parent versions.
- `Inventory` only depends on `Product`, so it works with any subclass without changes.
- File handling (`file_handler.py`) and the menu (`week8lab_oop_auditor.py`) are plain functions, not classes. `create_product()` in `file_handler.py` reads the saved `"type"` and creates the matching subclass.
