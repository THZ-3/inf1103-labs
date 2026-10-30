from can_be_shipped import CanBeShipped
from product import Product


class PhysicalProduct(Product, CanBeShipped):
    """A product that physically exists, has a weight and can be shipped."""

    BASE_SHIPPING_FEE = 5.00
    SHIPPING_RATE_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
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

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def to_dict(self):
        """Return the common product data plus the type and weight (used when saving)."""
        data = super().to_dict()
        data["type"] = "physical"
        data["weight"] = self.__weight
        return data

    def calculate_shipping_cost(self):
        """Shipping = $5.00 base fee + $2.00 per kg."""
        return self.BASE_SHIPPING_FEE + self.SHIPPING_RATE_PER_KG * self.__weight
