from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from file_handler import load_inventory, save_inventory
from physical_product import PhysicalProduct


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def add_product_menu(inventory):
    """Ask the user for a product type and its details, then add it to the inventory."""
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    product_type = input("Product Type: ").strip()
    if product_type not in ("1", "2"):
        print("Error: Invalid product type. Please choose 1 or 2.")
        return

    product_id = input("Product ID: ").strip()
    if not product_id:
        print("Error: Product ID cannot be empty!")
        return
    if inventory.search_product(product_id) is not None:
        print("Error: Product ID already exists!")
        return

    product_name = input("Product Name: ").strip()
    if not product_name:
        print("Error: Product name cannot be empty!")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        if product_type == "1":
            extra = float(input("Weight (kg): "))
        else:
            extra = float(input("Download Size (MB): "))
    except ValueError:
        print("Error: Invalid input. Please enter numbers for price, stock and weight/size.")
        return

    # Each product class checks its own data (negative price, stock, weight or size)
    try:
        if product_type == "1":
            product = PhysicalProduct(product_id, product_name, price, stock, extra)
        else:
            product = DigitalProduct(product_id, product_name, price, stock, extra)
    except ValueError as error:
        print(f"Error: {error}")
        return

    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock_menu(inventory):
    """Ask the user for a product ID and new stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
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


def search_product_menu(inventory):
    """Ask the user for a product ID and display the matching product."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()

    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    # Only products that implement the CanBeShipped interface have a shipping cost
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print("-" * 48)


def main():
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
