class Inventory:
    """Manages a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        """Add a product. Returns False if a product with the same ID already exists."""
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        """Return the Product with this ID, or None if it is not found."""
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def update_stock(self, product_id, quantity):
        """Update the stock of a product. Returns False if not found or the quantity is invalid."""
        product = self.search_product(product_id)
        if product is None:
            return False
        return product.update_stock(quantity)

    def display_all(self):
        """Print every product in the inventory."""
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        else:
            for product in self.__products:
                product.display_information()
        print("-" * 48)

    def get_products(self):
        """Return a copy of the product list so callers cannot change the inventory directly."""
        return list(self.__products)
