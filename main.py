from product import Product, LimitedProduct, NonStockedProduct
from store import Store
from promotion import SecondHalfPrice, ThirdOneFree, PercentDiscount

def make_order(store: Store):
    """Handles the process of creating an order and buying products."""
    shopping_list = []
    products = store.get_all_products()

    if not products:
        print("No active products in the store")
        return

    print("-----")
    for i, product in enumerate(products):
        print(
            f"{i + 1}. {product.name}, Price: {product.price}, Quantity: {product.get_quantity()}"
        )
    print("-----")

    while True:
        print("When you want to finish order, enter empty text.")
        item = input("Which product # do you want? ")
        quantity_input = input("What amount do you want? ")
        if item.strip() == "":
            if quantity_input.strip() != "":
                print("Cannot add quantity without a product. Returning to menu.")
            break
        if quantity_input.strip() == "":
            break
        try:
            index = int(item) - 1
            if index < 0 or index >= len(products):
                print("Invalid product name.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue
        try:
            index_quantity = int(quantity_input)
            if index_quantity <= 0:
                print("Quantity needs to be positive.\n")
                continue
            shopping_list.append((products[index], index_quantity))
            print("Product added to list!\n")
        except ValueError:
            print("Please enter a valid number")
    if shopping_list:
        try:
            total = store.order(shopping_list)
            print(f"Order made! Total payment: ${total}")
        except Exception as e:
            print(f"Error processing order: {e}")
    else:
        print("No product were added to the order")


def start(store: Store):
    while True:
        print("\nMenu")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ")

        if choice == "1":
            print("-----")
            for products in store.get_all_products():
                products.show()
            print("-----")
        elif choice == "2":
            print(f"Total of {store.get_total_quantity()} items in store")
        elif choice == "3":
            make_order(store)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


def main():
    bose = Product("Bose Headphones", 250, 500)
    mac = Product("MacBook Air M2", 1450, 100)
    cable = Product("USB-C Cable", 10, 200)
    ebook = NonStockedProduct("Python E‑Book", 30)
    ps5 = LimitedProduct("PlayStation 5", 600, 5, maximum=1)
    second_half_price = SecondHalfPrice("Second Half Price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", 30)
    bose.set_promotion(second_half_price)
    mac.set_promotion(third_one_free)
    ebook.set_promotion(thirty_percent)
    store = Store([bose, mac, cable, ebook, ps5])
    start(store)


if __name__ == "__main__":
    main()
