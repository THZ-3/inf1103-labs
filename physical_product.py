from product import Product


class PhysicalProduct(Product):
    """A product that physically exists and has a weight."""

    def __init__(self, product_id, name, price, stock, weight):
        # Reuse Product's constructor for the common attributes
        super().__init__(product_id, name, price, stock)

        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        """Print the common product information, then the weight."""
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")
