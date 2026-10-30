from digital_product import DigitalProduct
from physical_product import PhysicalProduct

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
