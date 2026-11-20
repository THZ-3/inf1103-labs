import csv
import json
import os

from inventory import Inventory
from product import Product
from product_factory import ProductFactory
from supplier import Supplier

FILENAME: str = "inventory.json"

UNKNOWN_SUPPLIER_DATA: dict = {"supplier_id": "S000", "name": "Unknown Supplier", "contact_email": ""}


def get_supplier(supplier_data: dict, suppliers: dict[str, Supplier]) -> Supplier:
    supplier_id = supplier_data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, supplier_data["name"],
                                          supplier_data["contact_email"])
    return suppliers[supplier_id]


def create_product(product_id: str, details: dict, suppliers: dict[str, Supplier]) -> Product:
    supplier = get_supplier(details.get("supplier", UNKNOWN_SUPPLIER_DATA), suppliers)
    return ProductFactory.create(details.get("type", "physical"), product_id, details["name"],
                                 details["price"], details["stock"], supplier,
                                 weight=details.get("weight", 0.0),
                                 download_size=details.get("download_size", 0.0))


def backup_unreadable_file(filename: str) -> None:
    try:
        os.replace(filename, filename + ".bak")
        print(f"The unreadable file was backed up to {filename}.bak.")
    except OSError:
        print(f"Warning: could not back up {filename}. Saving will overwrite it.")


def load_inventory(filename: str = FILENAME) -> Inventory:
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print(f"{filename} not found. Initializing with empty inventory.")
        return Inventory()
    except PermissionError:
        print(f"Error: no permission to read {filename}. Initializing with empty inventory.")
        return Inventory()

    inventory = Inventory()
    try:
        with file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError(f"{filename} does not contain a dictionary")

        suppliers: dict[str, Supplier] = {}
        for product_id, details in data.items():
            inventory.add_product(create_product(product_id, details, suppliers))
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
    except KeyError as error:
        print(f"Error: a product in {filename} is missing the field {error}.")
    except (ValueError, TypeError) as error:
        print(f"Error: {filename} contains invalid product data ({error}).")
    else:
        print("\nInventory loaded successfully.")
        return inventory

    print("Initializing with empty inventory.")
    backup_unreadable_file(filename)
    return Inventory()


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)
            for row_number, row in enumerate(reader, start=2):
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                except ValueError as error:
                    print(f"Skipping row {row_number}: {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {row_number}: product ID {product_id} already exists")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(inventory: Inventory, filename: str = FILENAME) -> None:
    data: dict = {}
    for product in inventory.get_products():
        data[product.get_product_id()] = product.to_dict()

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except OSError:
        print(f"Error: could not save to {filename}.")
