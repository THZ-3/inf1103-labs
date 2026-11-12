from digital_product import DigitalProduct
from inventory import Inventory
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

print("\n=== Section 3: Aggregation (Inventory and Product) ===")

print("\n1. Create a Product before any Inventory exists:")
amp = PhysicalProduct("P002", "Amplifier", 480.00, 3, guitar.get_supplier(), 12.0)
amp.display_information()

print("\n2. Add the Product to Inventory A:")
inventory_a = Inventory()
inventory_b = Inventory()
inventory_a.add_product(amp)
inventory_a.display_all()

print("\n3. Predict first: remove it from Inventory A, then use the Product:")
removed = inventory_a.remove_product("P002")
print(f"remove_product() returned the same object: {removed is amp}")
inventory_a.display_all()
amp.update_stock(10)
amp.display_information()
print("The Product still works after being removed from Inventory A.")

print("\n4. Add the same Product object to Inventory B:")
inventory_b.add_product(amp)
inventory_b.display_all()
print(f"Inventory B holds the same object: {inventory_b.find_product('P002') is amp}")

print("\n5. Empty Inventory B; the Products are not destroyed:")
inventory_b.add_product(guitar)
inventory_b.add_product(ebook)
for product in inventory_b.get_products():
    inventory_b.remove_product(product.get_product_id())
inventory_b.display_all()
for product in [amp, guitar, ebook]:
    product.display_information()

print(f"\nRemoving a product that is not there returns: {inventory_b.remove_product('X999')}")
