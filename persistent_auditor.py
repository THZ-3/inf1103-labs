inventory = 0
failed_entries = 0
deliveries_processed = 0
transaction_history = []

def load_inventory():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            inventory = int(lines[0].strip())

            history = []

            for line in lines[1:]:
                line = line.strip()

            if line != "":
                parts = line.split(",")
                product_name = parts[0]
                quantity = int(parts[1])
                history.append((product_name, quantity))

            return inventory, history

    except FileNotFoundError:
        return 0, []

def save_inventory(inventory, history):
    with open("inventory.txt", "w") as file:
        file.write(str(inventory) + "\n")

        for product_name, quantity in history:
            file.write(product_name + "," + str(quantity) + "\n")

    print("Inventory successfully saved to inventory.txt")


def get_valid_input():

    product_name = input("Enter Product Name or Enter 'quit' to stop:")

    if product_name.lower() == "quit":
        return "quit"

    if product_name == "":
        print("Error: Product name cannot be empty!")
        return None

    quantity = input("Enter Quantity: ")
    
    if not quantity.isdigit():
        print("Error: Invalid Input. Please enter an integer.")
        return None

    quantity = int(quantity)

    if quantity < 0:
        print("Error: quantity cannot be negative.")
        return None

    return product_name, quantity

def process_delivery(current_total, new_value):

    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):

    tax = amount*0.1
    return tax

def generate_report(inventory, failed_entries):

    print("\nReport")
    print("Total Units Processed:", inventory)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed Entries:", failed_entries)

inventory, transaction_history = load_inventory()

print("Current Inventory:", inventory)

if transaction_history:
    print("\nPrevious Transactions:")

    for product_name, quantity in transaction_history:
        print(product_name + "," + str(quantity))

while True:

    user_input = get_valid_input()

    if user_input == "quit":
        save_inventory(inventory, transaction_history)
        break

    if user_input is None:
        failed_entries += 1
        continue

    product_name, quantity = user_input

    inventory = process_delivery(inventory, quantity)

    tax = calculate_tax(quantity)

    transaction_history.append((product_name, quantity))

    deliveries_processed += 1

    print("\nNew Order Added: ")
    print(product_name + "," + str(quantity))
    print("Tax for this delivery: ", tax)
    print("Total Inventory: ", inventory)

    if inventory > 500:
        print("Alert: Overstock! Total inventory exceeds 500 units.")
        save_inventory(inventory, transaction_history)
        break

generate_report(inventory, failed_entries)

