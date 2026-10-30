from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product

# Lab 7, Steps 1-2: inheritance and method overriding
print("Physical product:")
guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, 3.5)
guitar.display_information()

print("\nDigital product:")
os_licence = DigitalProduct("D001", "Operating System", 199.99, 100, 4500)
os_licence.display_information()

# Inherited methods still work on the subclasses
print("\nInherited update_stock() on PhysicalProduct:")
guitar.update_stock(8)
print(f"Guitar stock is now {guitar.get_stock()}")

# Lab 7, Step 3: abstract class
print("\nget_fulfilment_info() from each subclass:")
print(f"Guitar: {guitar.get_fulfilment_info()}")
print(f"Operating System: {os_licence.get_fulfilment_info()}")

print("\nTrying to create a Product directly:")
try:
    generic = Product("X001", "Generic", 10.00, 1)
except TypeError as error:
    print(f"TypeError: {error}")

# Lab 7, Step 4: CanBeShipped interface
print("\nShipping costs for physical products of different weights:")
for item in [PhysicalProduct("P002", "Phone Case", 15.00, 50, 0.2),
             guitar,
             PhysicalProduct("P003", "Amplifier", 480.00, 3, 12.0)]:
    print(f"{item.get_name()} ({item.get_weight():.2f} kg): ${item.calculate_shipping_cost():.2f}")

print("\nWhich products can be shipped?")
for item in [guitar, os_licence]:
    print(f"{item.get_name()}: {isinstance(item, CanBeShipped)}")
