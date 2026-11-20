from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total


class StudentDiscount(PercentageDiscount):
    STUDENT_PERCENTAGE: float = 5

    def __init__(self) -> None:
        super().__init__(self.STUDENT_PERCENTAGE)
