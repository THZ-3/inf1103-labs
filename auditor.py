inventory = 0
failed_entries = 0


while True:
    stock = input("Enter a stock quantity or Enter 'quit' to stop : ")

    if stock.lower() == "quit":
        break

    if not stock.isdigit():
        print("Error: Invalid Input. Please enter an integer.")
        failed_entries += 1
        continue

    stock = int(stock)

    if stock < 0:
        print("Error: Stock quantity cannot be negative.")
        failed_entries +=1
        continue

    inventory += stock
    print("Total Inventory: ", inventory)

    if inventory > 500:
        print("Alert: Overstock! Total inventory exceeds 500 units.")
        break

print("\nReport")
print("Total Units Processed:", inventory)
print("Number of Failed Entries:", failed_entries)

