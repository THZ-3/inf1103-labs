import os

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from file_handler import load_inventory, save_inventory
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product

print("Physical product:")
guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, 3.5)
guitar.display_information()

print("\nDigital product:")
os_licence = DigitalProduct("D001", "Operating System", 199.99, 100, 4500)
os_licence.display_information()

print("\nInherited update_stock() on PhysicalProduct:")
guitar.update_stock(8)
print(f"Guitar stock is now {guitar.get_stock()}")

print("\nget_fulfilment_info() from each subclass:")
print(f"Guitar: {guitar.get_fulfilment_info()}")
print(f"Operating System: {os_licence.get_fulfilment_info()}")

print("\nTrying to create a Product directly:")
try:
    generic = Product("X001", "Generic", 10.00, 1)
except TypeError as error:
    print(f"TypeError: {error}")

print("\nShipping costs for physical products of different weights:")
for item in [PhysicalProduct("P002", "Phone Case", 15.00, 50, 0.2),
             guitar,
             PhysicalProduct("P003", "Amplifier", 480.00, 3, 12.0)]:
    print(f"{item.get_name()} ({item.get_weight():.2f} kg): ${item.calculate_shipping_cost():.2f}")

print("\nWhich products can be shipped?")
for item in [guitar, os_licence]:
    print(f"{item.get_name()}: {isinstance(item, CanBeShipped)}")

print("\nInventory operations with both product types:")
inventory = Inventory()
inventory.add_product(guitar)
inventory.add_product(os_licence)
print(f"Adding a duplicate ID is rejected: {not inventory.add_product(guitar)}")
print(f"Update stock through Inventory: {inventory.update_stock('D001', 75)}")
print(f"Search finds D001: {inventory.search_product('D001').get_name()}")
inventory.display_all()

print("\nJSON save and reload keeps the product types:")
test_file = "test_inventory.json"
save_inventory(inventory, test_file)
reloaded = load_inventory(test_file)
for item in reloaded.get_products():
    print(f"{item.get_product_id()}: {type(item).__name__}")
reloaded.display_all()
os.remove(test_file)
