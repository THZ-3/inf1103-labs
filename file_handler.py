import json
import os

from inventory import Inventory
from product import Product

FILENAME = "inventory.json"


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

        # Same format as Week 5: {"P001": {"name": ..., "price": ..., "stock": ...}}
        for product_id, details in data.items():
            product = Product(product_id, details["name"], details["price"], details["stock"])
            inventory.add_product(product)

        print("\nInventory loaded successfully.")
        return inventory
    except (json.JSONDecodeError, ValueError, KeyError, TypeError, OSError):
        print(f"Error reading {filename}. Initializing with empty inventory.")
        # Keep the unreadable file so a later save does not overwrite it
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
