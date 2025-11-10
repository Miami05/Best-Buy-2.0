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
        total_price = quantity * self.price
        self.set_quantity(self.quantity - quantity)
        return total_price
