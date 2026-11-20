import ast
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from file_handler import load_inventory, load_products
from input_helpers import get_non_empty_text, get_non_negative_int, get_positive_float
import oop_auditor
from inventory import Inventory
from supplier import Supplier

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_FILES = ["can_be_shipped.py", "digital_product.py", "discount.py", "file_handler.py",
                 "input_helpers.py", "inventory.py", "oop_auditor.py", "order.py",
                 "physical_product.py", "product.py", "product_factory.py", "supplier.py"]


def run_quietly(function, *args):
    output = io.StringIO()
    with redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue()


class TestInputHelpers(unittest.TestCase):
    def test_get_positive_float_asks_again_until_valid(self) -> None:
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            value, output = run_quietly(get_positive_float, "Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.splitlines(), ["Please enter a valid number, e.g. 12.50",
                                               "Please enter a number greater than zero."])

    def test_get_non_negative_int_asks_again_until_valid(self) -> None:
        with patch("builtins.input", side_effect=["ten", "-1", "3.5", "0"]):
            value, output = run_quietly(get_non_negative_int, "Stock: ")
        self.assertEqual(value, 0)
        self.assertEqual(len(output.splitlines()), 3)

    def test_get_non_empty_text_asks_again_until_valid(self) -> None:
        with patch("builtins.input", side_effect=["", "   ", "Desk Lamp"]):
            value, output = run_quietly(get_non_empty_text, "Name: ")
        self.assertEqual(value, "Desk Lamp")
        self.assertEqual(output.count("This field cannot be empty."), 2)


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S100", "CSV Supplier", "csv@example.com")

    def test_lab_sheet_file_loads_valid_rows_and_skips_bad_rows(self) -> None:
        path = os.path.join(PROJECT_DIR, "products.csv")
        _, output = run_quietly(load_products, path, self.inventory, self.supplier)
        self.assertEqual([product.get_product_id() for product in self.inventory.get_products()],
                         ["P001", "D001", "P003"])
        self.assertEqual(output.splitlines(), [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_missing_file_is_handled_gracefully(self) -> None:
        _, output = run_quietly(load_products, "no_such_file.csv", self.inventory, self.supplier)
        self.assertEqual(output.splitlines(), ["Products file not found: no_such_file.csv",
                                               "Load attempt finished."])
        self.assertEqual(self.inventory.get_products(), [])

    def test_bad_rows_are_skipped_and_valid_rows_still_load(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w") as file:
                file.write("product_type,product_id,name,price,stock_quantity\n"
                           "physical,P001,Lamp,0,5\n"
                           "digital,D001,App,9.99,-2\n"
                           "physical,P002,Chair,49.00\n"
                           "physical,P003,Stand,39.50,seven\n"
                           "digital,D002,Course,19.00,50\n"
                           "physical,P004,Desk,120.00,2\n"
                           "physical,P004,Desk Copy,120.00,2\n")
            _, output = run_quietly(load_products, path, self.inventory, self.supplier)
        self.assertEqual([product.get_product_id() for product in self.inventory.get_products()],
                         ["D002", "P004"])
        self.assertEqual(output.count("Skipping row"), 5)
        self.assertIn("2 products loaded.", output)


class TestLoadInventory(unittest.TestCase):
    def test_missing_inventory_file_gives_empty_inventory(self) -> None:
        inventory, output = run_quietly(load_inventory, "no_such_inventory.json")
        self.assertEqual(inventory.get_products(), [])
        self.assertIn("not found", output)

    def test_invalid_json_gives_empty_inventory_and_is_backed_up(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with open(path, "w") as file:
                file.write("{not valid json")
            inventory, output = run_quietly(load_inventory, path)
            self.assertTrue(os.path.exists(path + ".bak"))
        self.assertEqual(inventory.get_products(), [])
        self.assertIn("is not valid JSON", output)


class TestMenuClosedInput(unittest.TestCase):
    def check_menu_exits_gracefully(self, error: type[BaseException]) -> None:
        inventory = Inventory()
        with patch("oop_auditor.load_inventory", return_value=inventory), \
             patch("oop_auditor.save_inventory") as save, \
             patch("builtins.input", side_effect=error):
            _, output = run_quietly(oop_auditor.main)
        self.assertIn("Input was closed. Saving inventory before exit...", output)
        self.assertIn("Program terminated.", output)
        save.assert_called_once_with(inventory)

    def test_end_of_input_exits_gracefully(self) -> None:
        self.check_menu_exits_gracefully(EOFError)

    def test_ctrl_c_exits_gracefully(self) -> None:
        self.check_menu_exits_gracefully(KeyboardInterrupt)


class TestSpecificExceptions(unittest.TestCase):
    def test_every_except_names_a_specific_exception(self) -> None:
        for filename in PROJECT_FILES:
            with open(os.path.join(PROJECT_DIR, filename)) as file:
                tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    self.assertIsNotNone(node.type, f"bare except in {filename}")
                    names = [ast.unparse(item) for item in
                             (node.type.elts if isinstance(node.type, ast.Tuple) else [node.type])]
                    for name in names:
                        self.assertNotIn(name, ["Exception", "BaseException"],
                                         f"except {name} in {filename}")


if __name__ == "__main__":
    unittest.main()
