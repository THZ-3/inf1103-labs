from can_be_shipped import CanBeShipped
from file_handler import load_inventory, save_inventory
from input_helpers import (get_choice, get_non_empty_text, get_non_negative_float,
                           get_non_negative_int, get_positive_float)
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
    supplier_id = get_non_empty_text("Supplier ID: ")

    supplier = find_supplier(inventory, supplier_id)
    if supplier is not None:
        print(f"Using existing supplier: {supplier.get_name()}")
        return supplier

    print("New supplier.")
    supplier_name = get_non_empty_text("Supplier Name: ")
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
    product_type = get_choice("Product Type: ", PRODUCT_TYPES)

    while True:
        product_id = get_non_empty_text("Product ID: ")
        if inventory.find_product(product_id) is None:
            break
        print("That Product ID already exists. Please enter a different one.")

    product_name = get_non_empty_text("Product Name: ")
    price = get_positive_float("Price: ")
    stock = get_non_negative_int("Stock Quantity: ")

    weight = 0.0
    download_size = 0.0
    if product_type == "physical":
        weight = get_non_negative_float("Weight (kg): ")
    else:
        download_size = get_non_negative_float("Download Size (MB): ")

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

    new_stock = get_non_negative_int("\nNew Stock Quantity: ")

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
