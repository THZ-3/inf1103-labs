inventory = 0
failed_entries = 0
deliveries_processed = 0


def get_valid_input():

    stock = input("Enter a stock quantity or Enter 'quit' to stop : ")

    if stock.lower() == "quit":
        return "quit"

    if not stock.isdigit():
        print("Error: Invalid Input. Please enter an integer.")
        return None

    stock = int(stock)

    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        return None

    return stock

def process_delivery(current_total, new_value):

    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):

    tax = amount*0.1
    return tax

def generate_report(total_units, failed_attempts):

    print("\nReport")
    print("Total Units Processed:", inventory)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed Entries:", failed_entries)

while True:

    stock = get_valid_input()

    if stock == "quit":
        break

    if stock == None:
        failed_entries += 1
        continue

    inventory = process_delivery(inventory, stock)

    tax = calculate_tax(stock)

    deliveries_processed += 1

    print("Delivery Amount: ", stock)
    print("Tax for this delivery: ", tax)
    print("Total Inventory: ", inventory)

    if inventory > 500:
        print("Alert: Overstock! Total inventory exceeds 500 units.")
        break

generate_report(inventory, failed_entries)

