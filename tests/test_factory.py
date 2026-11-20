import unittest

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme", "acme@example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10,
                                        self.supplier, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 1.5)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100,
                                        self.supplier, download_size=800)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 800.0)

    def test_created_products_are_products(self) -> None:
        for product_type in ["physical", "digital"]:
            product = ProductFactory.create(product_type, "X001", "Item", 10.00, 1, self.supplier)
            self.assertIsInstance(product, Product)

    def test_passes_common_values_to_product(self) -> None:
        product = ProductFactory.create("physical", "P003", "Monitor Stand", 39.50, 7, self.supplier)
        self.assertEqual(product.get_product_id(), "P003")
        self.assertEqual(product.get_name(), "Monitor Stand")
        self.assertEqual(product.get_price(), 39.50)
        self.assertEqual(product.get_stock(), 7)
        self.assertIs(product.get_supplier(), self.supplier)

    def test_unknown_product_type_raises_clear_value_error(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Installation", 30.00, 5, self.supplier)
        self.assertEqual(str(context.exception), "Unknown product type: service")


if __name__ == "__main__":
    unittest.main()
