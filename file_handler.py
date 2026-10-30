import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct

FILENAME = "inventory.json"


def create_product(product_id, details):
    """Use the saved "type" to create the matching Product subclass."""
    # Lab 6 files have no "type"; those products were all physical
    product_type = details.get("type", "physical")

    if product_type == "physical":
        return PhysicalProduct(product_id, details["name"], details["price"],
                               details["stock"], details.get("weight", 0.0))
    if product_type == "digital":
        return DigitalProduct(product_id, details["name"], details["price"],
                              details["stock"], details["download_size"])
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(filename=FILENAME):
    """Load an Inventory from a JSON file, or return an empty Inventory if it cannot be read."""
    inventory = Inventory()

    if not os.path.exists(filename):
        print(f"{filename} not found. Initializing with empty inventory.")
        return inventory

    try:
        with open(filename, "r") as file:
            data = json.load(file)
        if not isinstance(data, dict):
            raise ValueError(f"{filename} does not contain a dictionary")

        for product_id, details in data.items():
            inventory.add_product(create_product(product_id, details))

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
    """Save every product in the Inventory to a JSON file."""
    data = {}
    for product in inventory.get_products():
        data[product.get_product_id()] = product.to_dict()

    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {filename}.")
    except OSError:
        print(f"Error: could not save to {filename}.")
