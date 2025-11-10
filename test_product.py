import pytest

from product import Product
from store import Store


class TestStore:
    """Test suite for Store class"""

    @pytest.fixture
    def sample_products(self):
        """Fixture to create sample products for testing"""
        return [
            Product("MacBook", 1450, 100),
            Product("Bose Earbuds", 250, 500),
            Product("Google Pixel", 500, 250),
        ]

    @pytest.fixture
    def store(self, sample_products):
        """Fixture to create a store with sample products"""
        return Store(sample_products)

    # Test initialization
    def test_store_initialization(self, sample_products):
        """Test store is initialized with products"""
        store = Store(sample_products)
        assert len(store.product) == 3

    def test_empty_store(self):
        """Test creating an empty store"""
        store = Store([])
        assert len(store.product) == 0
        assert store.get_total_quantity() == 0

    # Test adding/removing products
    def test_add_product(self, store):
        """Test adding a product to the store"""
        new_product = Product("iPhone", 999, 50)
        initial_count = len(store.product)

        store.add_product(new_product)
        assert len(store.product) == initial_count + 1
        assert new_product in store.product

    def test_remove_product(self, store, sample_products):
        """Test removing a product from the store"""
        product_to_remove = sample_products[0]
        initial_count = len(store.product)

        store.remove_product(product_to_remove)
        assert len(store.product) == initial_count - 1
        assert product_to_remove not in store.product

    def test_remove_nonexistent_product(self, store, capsys):
        """Test removing a product that doesn't exist"""
        fake_product = Product("Fake", 100, 10)
        store.remove_product(fake_product)

        captured = capsys.readouterr()
        assert "not found in store" in captured.out

    # Test getting products
    def test_get_all_products_active_only(self, sample_products):
        """Test that get_all_products returns only active products"""
        sample_products[1].deactivate()
        store = Store(sample_products)

        active_products = store.get_all_products()
        assert len(active_products) == 2
        assert sample_products[1] not in active_products

    def test_get_all_products_empty(self):
        """Test get_all_products on empty store"""
        store = Store([])
        assert store.get_all_products() == []

    # Test total quantity
    def test_get_total_quantity(self, store):
        """Test calculating total quantity of all products"""
        total = store.get_total_quantity()
        assert total == 850  # 100 + 500 + 250

    def test_get_total_quantity_includes_inactive(self, store, sample_products):
        """Test that total quantity includes inactive products"""
        sample_products[0].deactivate()
        total = store.get_total_quantity()
        assert total == 850  # Still counts inactive products

    def test_get_total_quantity_after_purchase(self, store, sample_products):
        """Test total quantity updates after purchases"""
        sample_products[0].buy(10)
        total = store.get_total_quantity()
        assert total == 840  # 90 + 500 + 250

    # Test order processing
    def test_order_single_product(self, store, sample_products):
        """Test ordering a single product"""
        shopping_list = [(sample_products[0], 5)]
        total = store.order(shopping_list)

        assert total == 7250.0  # 5 * 1450
        assert sample_products[0].get_quantity() == 95

    def test_order_multiple_products(self, store, sample_products):
        """Test ordering multiple products"""
        shopping_list = [
            (sample_products[0], 2),
            (sample_products[1], 3),
            (sample_products[2], 1),
        ]
        total = store.order(shopping_list)

        expected = (2 * 1450) + (3 * 250) + (1 * 500)
        assert total == expected
        assert sample_products[0].get_quantity() == 98
        assert sample_products[1].get_quantity() == 497
        assert sample_products[2].get_quantity() == 249

    def test_order_exceeds_quantity(self, store, sample_products, capsys):
        """Test ordering more than available quantity"""
        shopping_list = [(sample_products[0], 200)]
        total = store.order(shopping_list)

        assert total == 0  # Order should fail
        captured = capsys.readouterr()
        assert "Could not buy" in captured.out
        assert sample_products[0].get_quantity() == 100  # Unchanged

    def test_order_inactive_product(self, store, sample_products, capsys):
        """Test ordering an inactive product"""
        sample_products[0].deactivate()
        shopping_list = [(sample_products[0], 5)]
        total = store.order(shopping_list)

        assert total == 0
        captured = capsys.readouterr()
        assert "Could not buy" in captured.out

    def test_order_partial_success(self, store, sample_products, capsys):
        """Test order where some items succeed and some fail"""
        sample_products[1].deactivate()
        shopping_list = [
            (sample_products[0], 5),
            (sample_products[1], 2),
            (sample_products[2], 3),
        ]
        total = store.order(shopping_list)

        expected = (5 * 1450) + (3 * 500)
        assert total == expected
        captured = capsys.readouterr()
        assert "Could not buy Bose Earbuds" in captured.out

    def test_order_empty_list(self, store):
        """Test ordering with empty shopping list"""
        total = store.order([])
        assert total == 0

    # Test integration scenarios
    def test_product_deactivates_when_sold_out(self, store, sample_products):
        """Test that product deactivates when all stock is purchased"""
        shopping_list = [(sample_products[2], 250)]
        total = store.order(shopping_list)

        assert total == 125000.0
        assert sample_products[2].get_quantity() == 0
        assert sample_products[2].is_active() is False
        assert len(store.get_all_products()) == 2

    def test_multiple_orders(self, store, sample_products):
        """Test processing multiple sequential orders"""
        # First order
        order1 = [(sample_products[0], 10)]
        total1 = store.order(order1)
        assert total1 == 14500.0

        # Second order
        order2 = [(sample_products[0], 20)]
        total2 = store.order(order2)
        assert total2 == 29000.0

        assert sample_products[0].get_quantity() == 70

    def test_add_duplicate_product(self, store):
        """Test adding the same product instance multiple times"""
        new_product = Product("Tablet", 300, 20)
        store.add_product(new_product)
        store.add_product(new_product)

        assert store.product.count(new_product) == 2

    def test_order_with_same_product_multiple_times(self, store, sample_products):
        """Test ordering the same product multiple times in one order"""
        shopping_list = [(sample_products[0], 5), (sample_products[0], 10)]
        total = store.order(shopping_list)

        expected = (5 * 1450) + (10 * 1450)
        assert total == expected
        assert sample_products[0].get_quantity() == 85

    def test_store_with_all_inactive_products(self, sample_products):
        """Test store where all products are inactive"""
        for product in sample_products:
            product.deactivate()

        store = Store(sample_products)
        assert len(store.get_all_products()) == 0
        assert store.get_total_quantity() == 850

    def test_remove_all_products(self, store, sample_products):
        """Test removing all products from store"""
        # Create a copy to avoid iteration issues
        products_to_remove = sample_products.copy()
        for product in products_to_remove:
            store.remove_product(product)

        assert len(store.product) == 0
        assert store.get_total_quantity() == 0

    def test_order_updates_store_state(self, store, sample_products):
        """Test that order properly updates all store state"""
        initial_total = store.get_total_quantity()

        shopping_list = [(sample_products[1], 100)]
        store.order(shopping_list)

        new_total = store.get_total_quantity()
        assert new_total == initial_total - 100
        assert sample_products[1].get_quantity() == 400

    def test_large_order_value(self, store, sample_products):
        """Test ordering large quantities with high total value"""
        shopping_list = [
            (sample_products[0], 50),
            (sample_products[1], 200),
            (sample_products[2], 100),
        ]
        total = store.order(shopping_list)

        assert total == 172500.0
