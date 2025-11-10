import promotion


class Product:
    def __init__(self, name, price, quantity):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be a non empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non negative number")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non negative number")
        self.name = name
        self.price = float(price)
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self) -> int:
        """Return current quantity as int."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set quantity and deactivate product if it reaches 0."""
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non negative number")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        """Return whether the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def get_promotion(self):
        """Get the current promotion"""
        return self.promotion

    def set_promotion(self, promotion):
        """Set a promotion for a product"""
        self.promotion = promotion

    def show(self):
        """Print the product."""
        print(f"{self.name} , Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity) -> float:
        """
        Buy a given quantity. Returns total price.
        Raises Exception if product is inactive, quantity invalid,
                or not enough stock.
        """
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
        if not self.is_active():
            raise Exception("Cannot buy: the product is not avaible.")
        if quantity > self.quantity:
            raise Exception("Cannot buy: not enough stock avaible.")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self.active = True

    def show(self):
        """Show non-stocked product info."""
        print(f"{self.name}, Price: {self.price}")


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        """Show limited product info."""
        super().show()
        print(f"Maximum per purchase: {self.maximum}")
