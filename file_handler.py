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


def load_inventory(filename: str = FILENAME) -> Inventory:
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found. Initializing with empty inventory.")
        return inventory

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError(f"{filename} does not contain a dictionary")

        suppliers: dict[str, Supplier] = {}
        for product_id, details in data.items():
            inventory.add_product(create_product(product_id, details, suppliers))

        print("\nInventory loaded successfully.")
        return inventory
    except (json.JSONDecodeError, ValueError, KeyError, TypeError, OSError):
        print(f"Error reading {filename}. Initializing with empty inventory.")
        
        try:
            os.replace(filename, filename + ".bak")
            print(f"The unreadable file was backed up to {filename}.bak.")
        except OSError:
            print(f"Warning: could not back up {filename}. Saving will overwrite it.")
        return Inventory()


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
