import unittest

from discount import BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount, StudentDiscount
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class RecordingDiscount(DiscountStrategy):
    def __init__(self) -> None:
        self.received_total: float | None = None

    def apply(self, total: float) -> float:
        self.received_total = total
        return total / 2


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("S001", "Acme", "acme@example.com")
    desk = ProductFactory.create("physical", "P001", "Desk", 125.00, 10, supplier, weight=20)
    order = Order("O001", discount)
    order.add_order_line(desk, 2)
    return order


class TestDiscountStrategies(unittest.TestCase):
    def test_no_discount_returns_total_unchanged(self) -> None:
        self.assertEqual(NoDiscount().apply(250.0), 250.0)

    def test_percentage_discount_takes_percentage_off(self) -> None:
        self.assertAlmostEqual(PercentageDiscount(10).apply(250.0), 225.0)

    def test_bulk_discount_applies_at_or_above_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(250.0), 230.0)
        self.assertEqual(BulkDiscount(200, 20).apply(200.0), 180.0)

    def test_bulk_discount_does_not_apply_below_threshold(self) -> None:
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_bulk_discount_never_goes_below_zero(self) -> None:
        self.assertEqual(BulkDiscount(0, 50).apply(30.0), 0.0)

    def test_student_discount_takes_five_percent_off(self) -> None:
        self.assertAlmostEqual(StudentDiscount().apply(250.0), 237.5)

    def test_invalid_percentage_is_rejected(self) -> None:
        for percentage in [0, -10, 150]:
            with self.assertRaises(ValueError):
                PercentageDiscount(percentage)

    def test_invalid_bulk_discount_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            BulkDiscount(-1, 20)
        with self.assertRaises(ValueError):
            BulkDiscount(200, 0)


class TestOrderUsesStrategy(unittest.TestCase):
    def test_order_uses_no_discount_by_default(self) -> None:
        order = make_order_totalling_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250.0)

    def test_order_total_with_bulk_discount(self) -> None:
        self.assertEqual(make_order_totalling_250(BulkDiscount(200, 20)).calculate_total(), 230.0)

    def test_set_discount_changes_strategy_on_existing_order(self) -> None:
        order = make_order_totalling_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_order_passes_subtotal_to_strategy(self) -> None:
        strategy = RecordingDiscount()
        order = make_order_totalling_250(strategy)
        self.assertEqual(order.calculate_total(), 125.0)
        self.assertEqual(strategy.received_total, 250.0)

    def test_new_strategy_works_without_changing_order(self) -> None:
        order = make_order_totalling_250()
        order.set_discount(RecordingDiscount())
        self.assertEqual(order.calculate_total(), 125.0)

    def test_two_orders_can_share_one_strategy(self) -> None:
        shared = PercentageDiscount(10)
        first = make_order_totalling_250(shared)
        second = make_order_totalling_250(shared)
        self.assertIs(first.get_discount(), second.get_discount())


if __name__ == "__main__":
    unittest.main()
