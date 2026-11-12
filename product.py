from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
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
        self.__supplier: Supplier = supplier

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def get_supplier_id(self) -> str:
        return self.__supplier.get_supplier_id()

    def get_supplier_name(self) -> str:
        return self.__supplier.get_name()

    def update_stock(self, quantity):
        if quantity < 0:
            return False
        self.__stock = quantity
        return True

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock} | "
              f"Supplier: {self.__supplier.get_name()}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass

    def to_dict(self):
        return {
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict()
        }
