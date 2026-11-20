import unittest

from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class TestProductValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Acme", "acme@example.com")

    def test_price_of_zero_is_rejected(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("physical", "P001", "Lamp", 0, 5, self.supplier)
        self.assertEqual(str(context.exception), "Price must be greater than zero.")

    def test_negative_price_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "App", -5, 5, self.supplier)

    def test_negative_stock_is_rejected(self) -> None:
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("physical", "P001", "Lamp", 10, -1, self.supplier)
        self.assertEqual(str(context.exception), "Stock quantity cannot be negative.")

    def test_rules_apply_to_both_product_types(self) -> None:
        for product_type in ["physical", "digital"]:
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X001", "Item", 0, 1, self.supplier)
            with self.assertRaises(ValueError):
                ProductFactory.create(product_type, "X001", "Item", 10, -1, self.supplier)

    def test_smallest_valid_values_are_accepted(self) -> None:
        product = ProductFactory.create("digital", "D001", "App", 0.01, 0, self.supplier)
        self.assertEqual(product.get_price(), 0.01)
        self.assertEqual(product.get_stock(), 0)

    def test_update_stock_rejects_negative_without_changing_stock(self) -> None:
        product = ProductFactory.create("digital", "D001", "App", 5, 3, self.supplier)
        self.assertFalse(product.update_stock(-1))
        self.assertEqual(product.get_stock(), 3)


class TestOrderLineValidation(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "Acme", "acme@example.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp", 10, 5, supplier)

    def test_zero_or_negative_quantity_is_rejected(self) -> None:
        for quantity in [0, -3]:
            order = Order("O001")
            with self.assertRaises(ValueError) as context:
                order.add_order_line(self.product, quantity)
            self.assertEqual(str(context.exception), "Quantity must be greater than zero.")
            self.assertEqual(order.get_order_lines(), [])

    def test_positive_quantity_is_accepted(self) -> None:
        order = Order("O001")
        order.add_order_line(self.product, 1)
        self.assertEqual(len(order.get_order_lines()), 1)


if __name__ == "__main__":
    unittest.main()
