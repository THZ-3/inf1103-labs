from can_be_shipped import CanBeShipped
from file_handler import load_inventory, save_inventory
from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

PRODUCT_TYPES: dict[str, str] = {"1": "physical", "2": "digital"}


def display_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    for product in inventory.get_products():
        if product.get_supplier_id() == supplier_id:
            return product.get_supplier()
    return None


def choose_supplier(inventory: Inventory) -> Supplier | None:
    supplier_id = input("Supplier ID: ").strip()
    if not supplier_id:
        print("Error: Supplier ID cannot be empty!")
        return None

    supplier = find_supplier(inventory, supplier_id)
    if supplier is not None:
        print(f"Using existing supplier: {supplier.get_name()}")
        return supplier

    print("New supplier.")
    supplier_name = input("Supplier Name: ").strip()
    contact_email = input("Supplier Email: ").strip()
    try:
        return Supplier(supplier_id, supplier_name, contact_email)
    except ValueError as error:
        print(f"Error: {error}")
        return None


def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    choice = input("Product Type: ").strip()
    if choice not in PRODUCT_TYPES:
        print("Error: Invalid product type. Please choose 1 or 2.")
        return
    product_type = PRODUCT_TYPES[choice]

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Error: Product ID cannot be empty!")
        return
    if inventory.find_product(product_id) is not None:
        print("Error: Product ID already exists!")
        return

    product_name = input("Product Name: ").strip()
    if not product_name:
        print("Error: Product name cannot be empty!")
        return

    weight = 0.0
    download_size = 0.0
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "physical":
            weight = float(input("Weight (kg): "))
        else:
            download_size = float(input("Download Size (MB): "))
    except ValueError:
        print("Error: Invalid input. Please enter numbers for price, stock and weight/size.")
        return

    supplier = choose_supplier(inventory)
    if supplier is None:
        return

    try:
        product = ProductFactory.create(product_type, product_id, product_name, price, stock,
                                        supplier, weight=weight, download_size=download_size)
    except ValueError as error:
        print(f"Error: {error}")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("\nNew Stock Quantity: "))
    except ValueError:
        print("Error: Invalid input. Please enter an integer.")
        return

    if inventory.update_stock(product_id, new_stock):
        print("\nStock updated successfully!")
    else:
        print("Error: Stock cannot be negative.")


def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.find_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    print(f"    Supplier Email: {product.get_supplier().get_contact_email()}")
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    display_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Error: Invalid option. Please choose a number between 1 and 6.")


if __name__ == "__main__":
    main()
