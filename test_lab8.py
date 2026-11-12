from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from supplier import Supplier

print("=== Section 2: Association (Supplier and Product) ===")

print("\n1. Create a Supplier on its own:")
supplier = Supplier("S001", "Acme Music", "sales@acmemusic.com")
supplier.display_information()

print("\n2. Create a PhysicalProduct and a DigitalProduct using that Supplier:")
guitar = PhysicalProduct("P001", "Guitar", 350.00, 5, supplier, 3.5)
ebook = DigitalProduct("D001", "Guitar eBook", 15.00, 100, supplier, 20)
guitar.display_information()
ebook.display_information()

print("\n3. Display the supplier information through each Product:")
guitar.get_supplier().display_information()
ebook.get_supplier().display_information()

print("\n4. Supplier and Products are separate objects:")
print(f"Both products refer to the same Supplier object: {guitar.get_supplier() is ebook.get_supplier()}")
print(f"The Supplier is not one of the Products: {guitar.get_supplier() is not guitar}")
print(f"id(supplier) = {id(supplier)}, id(guitar) = {id(guitar)}, id(ebook) = {id(ebook)}")

print("\n5. Predict first: delete the supplier variable, then use the Products:")
del supplier
guitar.get_supplier().display_information()
ebook.get_supplier().display_information()
print("Both products can still reach their supplier.")
