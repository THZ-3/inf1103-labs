import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from supplier import Supplier

FILENAME = "inventory.json"

UNKNOWN_SUPPLIER_DATA = {"supplier_id": "S000", "name": "Unknown Supplier", "contact_email": ""}


def get_supplier(supplier_data, suppliers):
    supplier_id = supplier_data["supplier_id"]
    if supplier_id not in suppliers:
        suppliers[supplier_id] = Supplier(supplier_id, supplier_data["name"],
                                          supplier_data["contact_email"])
    return suppliers[supplier_id]


def create_product(product_id, details, suppliers):
    product_type = details.get("type", "physical")
    supplier = get_supplier(details.get("supplier", UNKNOWN_SUPPLIER_DATA), suppliers)

    if product_type == "physical":
        return PhysicalProduct(product_id, details["name"], details["price"],
                               details["stock"], supplier, details.get("weight", 0.0))
    if product_type == "digital":
        return DigitalProduct(product_id, details["name"], details["price"],
                              details["stock"], supplier, details["download_size"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(filename=FILENAME):
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found. Initializing with empty inventory.")
        return inventory

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError(f"{filename} does not contain a dictionary")

        suppliers = {}
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


def save_inventory(inventory, filename=FILENAME):
    data = {}
    for product in inventory.get_products():
        data[product.get_product_id()] = product.to_dict()

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except OSError:
        print(f"Error: could not save to {filename}.")
