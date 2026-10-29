class Product:
    
    def __init__(self, product_id, name, price, stock):
        if not product_id:
            raise ValueError("Product ID cannot be empty.")
        if not name:
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")

        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def get_product_id(self):
        return self.product_id

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_stock(self):
        return self.stock

    def update_stock(self, quantity):
        """Set a new stock quantity. Returns True if the update was accepted."""
        if quantity < 0:
            return False
        self.stock = quantity
        return True

    def display_information(self):
        
        print(f"ID: {self.product_id} | Name: {self.name} | "
              f"Price: ${self.price:.2f} | Stock: {self.stock}")

    def to_dict(self):
        """Return the product's data as a dictionary."""
        return {
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
