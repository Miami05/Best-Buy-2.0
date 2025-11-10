from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstract base class for promotions."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Apply the promotion to a product purchase.

        Args:
            product: The Product instance
            quantity: The quantity being purchased

        Returns:
            float: The discounted total price
        """
        pass


class PercentDiscount(Promotion):
    """Applies a percentage discount to the total price."""

    def __init__(self, name, percent):
        """
        Initialize percentage discount promotion.

        Args:
            name: Name of the promotion
            percentage: Discount percentage (e.g., 20 for 20% off)
        """
        super().__init__(name)
        if not isinstance(percent, (int, float)) or not 0 <= percent <= 100:
            raise ValueError("Percentage must be between 0 and 100")
        self.percentage = percent

    def apply_promotion(self, product, quantity) -> float:
        """Apply percentage discount to total price"""
        total_price = product.price * quantity
        discount_amount = total_price * (self.percentage / 100)
        return total_price - discount_amount


class SecondHalfPrice(Promotion):
    """Second item at half price promotion."""

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply second item at half price.
        For every 2 items, one is full price and one is half price.
        """
        full_price_items = (quantity + 1) // 2
        half_priced_items = quantity // 2
        total_price = (full_price_items * product.price) + (
            half_priced_items * product.price * 0.5
        )
        return total_price


class ThirdOneFree(Promotion):
    """Buy 2, get 1 free promotion."""

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """
        Apply buy 2 get 1 free promotion.
        For every 3 items, customer pays for only 2.
        """
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price
