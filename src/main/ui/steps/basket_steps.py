import allure

from playwright.sync_api import Page
from src.main.ui.pages.basket_page import BasketPage



class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Проверяем что товар {item_name} в корзине")
    def check_item_in_cart(self, item_name: str):
        self.basket.check_item_in_cart(item_name)
        return self

    @allure.step("Проверяем отсутствие товара в корзине")
    def check_miss_item_in_cart(self, item_name: str):
        self.basket.check_miss_item_in_cart(item_name)
        return self

    @allure.step("Получаем список товаров в корзине")
    def get_items_in_cart(self) -> list[str]:
        return self.basket.get_products_names_in_cart()

    @allure.step("Получаем сумму товаров в корзине")
    def get_items_total_in_cart(self) -> float:
        return self.basket.summ_in_cart()

    @allure.step("Удаляем товар из корзины")
    def remove_items_in_cart(self, item_name: str):
        self.basket.remove_products_in_cart(item_name)
        return self

    @allure.step("Нажимаем на Checkout")
    def click_checkout(self):
        self.basket.click_checkout_button()
        return self
