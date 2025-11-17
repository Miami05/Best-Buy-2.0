class Product:
    def __init__(self, name, price, quantity):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non negative number")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non negative number")
        self.name = name
        self._price = float(price)
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def quantity(self):
        """Get current quantity."""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Set quantity and deactivate product if it reaches 0."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non negative number")
        self._quantity = quantity
        if self._quantity == 0:
            self.active = False

    @property
    def price(self):
        """Get current price."""
        return self._price

    @price.setter
    def price(self, price):
        """Set price with validation."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non negative number")
        self._price = float(price)

    @property
    def active(self):
        """Get active status."""
        return self._active

    @active.setter
    def active(self, status):
        """Set active status."""
        self._active = status

    @property
    def promotion(self):
        """Get the current promotion."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        """Set a promotion for the product."""
        self._promotion = promotion

    def get_quantity(self) -> int:
        """Return current quantity as int (kept for backward compatibility)."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set quantity (kept for backward compatibility)."""
        self.quantity = quantity

    def is_active(self) -> bool:
        """Return whether the product is active (kept for backward compatibility)."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def get_promotion(self):
        """Get the current promotion (kept for backward compatibility)."""
        return self.promotion

    def set_promotion(self, promotion):
        """Set a promotion (kept for backward compatibility)."""
        self.promotion = promotion

    def __str__(self):
        """String representation of the product."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{promotion_info}"

    def show(self):
        """Print the product (kept for backward compatibility)."""
        print(self)

    def __gt__(self, other):
        """Compare products by price using > operator."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def __lt__(self, other):
        """Compare products by price using < operator."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def buy(self, quantity) -> float:
        """
        Buy a given quantity. Returns total price.
        Applies promotion if available.
        Raises Exception if product is inactive, quantity invalid,
                or not enough stock.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not self.active:
            raise Exception("Cannot buy: the product is not avaible.")
        if quantity > self.quantity:
            raise Exception("Cannot buy: not enough stock avaible.")

        # Apply promotion if available, otherwise use regular price
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self.quantity = self.quantity - quantity
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self._active = True

    def __str__(self):
        """String representation of non-stocked product."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}{promotion_info}"

    def show(self):
        """Show non-stocked product info."""
        print(self)

    def buy(self, quantity) -> float:
        """
        Buy non-stocked product (always available).
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not self.active:
            raise Exception("Cannot buy: the product is not avaible.")

        # Apply promotion if available
        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        return total_price


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def __str__(self):
        """String representation of limited product."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{promotion_info}\nMaximum per purchase: {self.maximum}"

    def show(self):
        """Show limited product info."""
        print(self)

    def buy(self, quantity) -> float:
        """
        Buy a given quantity with maximum limit enforcement.
        Returns total price with promotion applied if available.
        """
        if not instance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if quantity > self.maximum:
            raise Exception(f"Cannot buy: maximum purchase limit is {self.maximum}.")
        return super().buy(quantity)
