class Product:
    """Represents and manages a single product in the inventory."""

    def __init__(self, product_id, name, price, stock):
        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set a new stock quantity. Returns True if the update was accepted."""
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        """Print this product on a single line."""
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        """Return the product's data as a dictionary (used when saving)."""
        return {
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock
        }
