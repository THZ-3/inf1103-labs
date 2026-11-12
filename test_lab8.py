from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
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

print("\n=== Section 4: Composition (Order and OrderLine) ===")

print("\n1. Create an Order and add two products with add_order_line():")
order_1 = Order("O001")
order_1.add_order_line(guitar, 2)
order_1.add_order_line(ebook, 3)

print("\n2. Display each order line and the order total:")
order_1.display_information()

print("\n3. Predict first: add the same Product to a different Order:")
order_2 = Order("O002")
order_2.add_order_line(guitar, 1)
order_2.display_information()

line_1 = order_1.get_order_lines()[0]
line_2 = order_2.get_order_lines()[0]
print(f"\nThe two orders have different OrderLine objects: {line_1 is not line_2}")
print(f"id(line_1) = {id(line_1)}, id(line_2) = {id(line_2)}")
print(f"Both OrderLines refer to the same Product object: {line_1.get_product() is line_2.get_product() is guitar}")
print(f"id(line_1 product) = {id(line_1.get_product())}, id(line_2 product) = {id(line_2.get_product())}")
print("So: 2 OrderLine objects, but only 1 Product object.")
del line_1, line_2

print("\n4. Remove an order line through the Order:")
print(f"remove_order_line('D001') returned: {order_1.remove_order_line('D001')}")
order_1.display_information()
print("The eBook Product still exists:")
ebook.display_information()

print("\n5. Remove Order O002 from the scenario:")
del order_2
print("Order O002 and its OrderLine are gone, but the Guitar Product is not:")
guitar.display_information()

print("\n6. An OrderLine cannot be added with an invalid quantity:")
try:
    order_1.add_order_line(guitar, 0)
except ValueError as error:
    print(f"ValueError: {error}")

print("\n=== Section 6: Liskov Substitution Principle ===")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


print("\n1. The same function works with a PhysicalProduct and a DigitalProduct:")
show_product_details(guitar)
show_product_details(ebook)

print("\n2. Both product types work with the normal Inventory operations:")
shop = Inventory()
print(f"add_product(guitar): {shop.add_product(guitar)}")
print(f"add_product(ebook): {shop.add_product(ebook)}")
print(f"find_product('D001') is ebook: {shop.find_product('D001') is ebook}")
print(f"update_stock('P001', 6): {shop.update_stock('P001', 6)}")
print(f"update_stock('D001', 90): {shop.update_stock('D001', 90)}")
shop.display_all()
print(f"remove_product('P001') is guitar: {shop.remove_product('P001') is guitar}")
shop.display_all()

print("\n3. Both subclasses keep Product's update_stock() expectation:")
print("   accepts any quantity >= 0 and returns True, rejects a negative and returns False")
for product in [guitar, ebook]:
    before = product.get_stock()
    accepted = product.update_stock(0)
    zero_stock = product.get_stock()
    product.update_stock(before)
    rejected = product.update_stock(-5)
    print(f"{type(product).__name__}: update_stock(0) -> {accepted} (stock {zero_stock}), "
          f"update_stock(-5) -> {rejected} (stock still {product.get_stock()})")


print("\n4. Diagnose: a DigitalProduct that refuses update_stock() breaks Inventory:")


class NoStockDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> bool:
        raise NotImplementedError("Digital products have no stock")


licence = NoStockDigitalProduct("D002", "Software Licence", 50.00, 10, guitar.get_supplier(), 300)
shop.add_product(licence)
try:
    shop.update_stock("D002", 20)
except NotImplementedError as error:
    print(f"Inventory.update_stock() crashed: NotImplementedError: {error}")
print("Inventory only knows it has a Product, so this subclass cannot safely replace Product.")

print("\n=== Section 7: Polymorphism ===")

print("\n1. Add physical and digital products to the same Inventory:")
store = Inventory()
store.add_product(guitar)
store.add_product(ebook)
store.add_product(amp)
print(f"Products in the store: {[product.get_name() for product in store.get_products()]}")

print("\n2. Predict first: one loop, no isinstance(), same method calls on every Product:")
for product in store.get_products():
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")

print("\n3. The same show_product_details(product: Product) function from Section 6:")
for product in store.get_products():
    show_product_details(product)

print("\n=== Section 9: Testing checklist ===")

results: list[bool] = []


def check(description: str, passed: bool) -> None:
    results.append(passed)
    print(f"[{'PASS' if passed else 'FAIL'}] {description}")


beat_co = Supplier("S002", "Beat Co", "beat@co.com")
drum = PhysicalProduct("P010", "Drum", 500.00, 2, beat_co, 20)
course = DigitalProduct("D010", "Drum Course", 49.00, 100, beat_co, 800)

check("Supplier and Product are separate objects that exist independently",
      drum.get_supplier() is beat_co and drum is not beat_co)
check("Product stores a reference to its Supplier",
      drum.get_supplier() is course.get_supplier() is beat_co)

warehouse_1 = Inventory()
warehouse_2 = Inventory()
warehouse_1.add_product(drum)
check("Inventory aggregates Product objects", warehouse_1.find_product("P010") is drum)
moved = warehouse_1.remove_product("P010")
warehouse_2.add_product(drum)
check("A Product can move to another Inventory without being destroyed",
      moved is drum and warehouse_1.find_product("P010") is None
      and warehouse_2.find_product("P010") is drum and drum.get_name() == "Drum")

order_a = Order("O010")
order_b = Order("O011")
order_a.add_order_line(drum, 2)
order_a.add_order_line(course, 1)
order_b.add_order_line(drum, 1)
lines_a = order_a.get_order_lines()
check("Order creates and manages its own OrderLine objects",
      len(lines_a) == 2 and lines_a[0] is not order_b.get_order_lines()[0])
check("OrderLine refers to a Product but does not own it",
      lines_a[0].get_product() is drum and order_b.get_order_lines()[0].get_product() is drum)
check("Order calculates its total from its OrderLines",
      order_a.calculate_total() == sum(line.calculate_subtotal() for line in lines_a) == 1049.00)
del lines_a

warehouse_2.add_product(course)
check("Inventory works with both product types through Product",
      all(isinstance(product, Product) for product in warehouse_2.get_products())
      and len(warehouse_2.get_products()) == 2)
check("Both subclasses keep update_stock() behaviour",
      all(product.update_stock(5) and not product.update_stock(-1) and product.get_stock() == 5
          for product in [drum, course]))
check("Polymorphic calls run the correct subclass implementation",
      [product.get_fulfilment_info() for product in warehouse_2.get_products()]
      == ["This product requires physical shipping.", "This product is delivered digitally via download."])

print(f"\n{sum(results)} of {len(results)} checks passed.")
