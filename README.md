# Best-Buy-2.0

A feature-rich Python store simulator—explore product management, order processing, and discounts with advanced product and promotion types. Perfect for practicing object-oriented programming and classic business logic.

## Features

- **Multiple Product Types:** Regular, limited-stock, and non-stocked (digital/gift cards).
- **Promotions Engine:** Built-in promotions like "Buy 2, get next half off", "3 for 2", and percent discounts.
- **CLI Store Simulator:** Interactive menu for viewing products, checking inventory, and making orders.
- **Inventory Tracking:** Stock management, including quantity limits for special products.
- **Extensible Classes:** Easy to add custom products and promotions using inheritance.

## Project Structure

Best-Buy-2.0/  
├── main.py # Main menu + order logic  
├── product.py # Base + child Product classes  
├── promotion.py # Promotion types and logic  
├── store.py # Store class and inventory/order management  
├── requirements.txt # (If needed for external deps)  
├── test_product.py # (Unit tests for products/promotions)  
└── **pycache**/ # Ignore

## Getting Started

1. **Clone the repo:**
```bash
git clone https://github.com/Miami05/Best-Buy-2.0.git
```
```bash
cd Best-Buy-2.0
```

2. **Run the main script:**
```bash
python main.py
```

3. **Follow the interactive menu:**
- List all products and available discounts
- See store totals
- Make multi-item orders, experience promotions in action!

## Example Product Types

- **Product:** Standard item (e.g., USB-C Cable)
- **LimitedProduct:** Limited stock with per-order maximum (e.g., PlayStation 5, 1 per order)
- **NonStockedProduct:** Always available, no physical stock (e.g., E‑Books)
- **Promotions:**  
- Second item half price
- Third item free
- Percent (%) discount

## Extending

- Add more product subclasses for different business rules.
- Add/extend promotion logic in `promotion.py`.
- Use `test_product.py` for practicing unit tests.

## License

Open-source project for learning and personal use.

Experiment with Best-Buy-2.0 to master OOP patterns and shop logic in Python!
