
from src.main.ui.steps.checout_steps import CheckoutSteps
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps



def test_add_item_and_check_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.click_cart_button()
    basket.check_item_in_cart("Sauce Labs Backpack")


def test_add_item_SLFJ_and_SLBT_in_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog.click_cart_button()
    item_names = basket.get_items_in_cart()
    for item_name in item_names:
        assert item_name in ["Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt"]


def test_remove_item_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.click_cart_button()
    basket.check_item_in_cart("Sauce Labs Fleece Jacket")
    basket.remove_items_in_cart("Sauce Labs Fleece Jacket")
    basket.check_miss_item_in_cart("Sauce Labs Fleece Jacket")


def test_remove_all_items_from_cart(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    catalog.click_cart_button()
    item_names = basket.get_items_in_cart()
    for item_name in item_names:
        assert item_name in ["Sauce Labs Backpack", "Test.allTheThings() T-Shirt (Red)"]
        basket.remove_items_in_cart(item_name)
        basket.check_miss_item_in_cart(item_name)


def test_e_2_e(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog.click_cart_button()
    item_names = basket.get_items_in_cart()
    for item_name in item_names:
        assert item_name in ["Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt"]
    total_summ = basket.get_items_total_in_cart()
    basket.click_checkout()
    checkout.start_checkout(first_name = "Ivan", last_name = "Ivanov", postal_code = "111")
    assert checkout.get_item_total_after_continue() == total_summ
    checkout.finish_checkout()
    assert checkout.get_massage() == "Thank you for your order!"


def test_checkout_without_items(page):
    login = LoginSteps(page)
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    login.open_login_page().login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.click_cart_button()
    basket.check_item_in_cart("Sauce Labs Fleece Jacket")
    basket.click_checkout()
    checkout.start_checkout(first_name = "Ivan", last_name = "Ivanov", postal_code = "")
    assert checkout.get_error_text() == "Error: Postal Code is required"
