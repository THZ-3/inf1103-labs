import json
import os

def display_all(inventory):
    """Display all products in the inventory."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    else:
        for prod_id, details in inventory.items():
            print(f"ID: {prod_id} | Name: {details['name']} | Price: ${details['price']:.2f} | Stock: {details['stock']}")
    print("-" * 48)

def add_product(inventory):
    """Add a new product to the inventory dictionary."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    
    if product_id in inventory:
        print("Error: Product ID already exists!")
        return

    product_name = input("Product Name: ").strip()
    if not product_name:
        print("Error: Product name cannot be empty!")
        return

    try:
        price = float(input("Price: "))
        if price < 0:
            print("Error: Price cannot be negative.")
            return
            
        stock = int(input("Stock Quantity: "))
        if stock < 0:
            print("Error: Stock quantity cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid input. Please enter numbers for price and stock.")
        return

    inventory[product_id] = {
        "name": product_name,
        "price": price,
        "stock": stock
    }
    print("\nProduct added successfully!")

def update_stock(inventory):
    """Update stock quantity for an existing product ID."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    
    if product_id in inventory:
        product = inventory[product_id]
        print("\nProduct Found:")
        print(f"Name: {product['name']}")
        print(f"Current Stock: {product['stock']}")
        
        try:
            new_stock = int(input("\nNew Stock Quantity: "))
            if new_stock < 0:
                print("Error: Stock cannot be negative.")
                return
            product['stock'] = new_stock
            print("\nStock updated successfully!")
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")
    else:
        print("Product not found.")

def search_product(inventory):
    """Search for a product by its ID and display its details."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    
    if product_id in inventory:
        product = inventory[product_id]
        print("\nProduct Found")
        print("-" * 48)
        print(f"ID: {product_id}")
        print(f"Name: {product['name']}")
        print(f"Price: ${product['price']:.2f}")
        print(f"Stock: {product['stock']}")
        print("-" * 48)
    else:
        print("Product not found.")

def load_inventory():
    """Load inventory from inventory.json if it exists, otherwise return an empty inventory."""
    if os.path.exists("inventory.json"):
        try:
            print("inventory.json found.")
            with open("inventory.json", "r") as file:
                inventory = json.load(file)
                print("\nInventory loaded successfully.")
                return inventory
        except json.JSONDecodeError:
            print("Error reading inventory.json. Initializing with empty inventory.")
    
    print("inventory.json not found. Initializing with empty inventory.")
    return {}

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()

    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
        elif option == "6":
            print("\nProgram terminated.")
            break
        else:
            print("Error: Invalid option. Please choose a number between 1 and 6.")

if __name__ == "__main__":
    main()