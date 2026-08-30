from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage



class BasketPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_info = page.locator(".cart_item")
        self.checkout_button = page.locator("#checkout")

    def check_item_in_cart(self, product_name: str):
        card = self.cart_info.filter(has_text = product_name)
        expect(card).to_be_visible()

    def check_miss_item_in_cart(self, product_name: str):
        card = self.cart_info.filter(has_text = product_name)
        expect(card).not_to_be_visible()

    def get_products_names_in_cart(self) -> list[str]:
        return self.cart_info.locator(".inventory_item_name").all_text_contents()

    def remove_products_in_cart(self, product_name: str):
        card = self.cart_info.filter(has_text = product_name)
        card.locator(".cart_button").click()

    def get_products_prices_in_cart(self) -> list[float]:
        prices = self.cart_info.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices]

    def summ_in_cart(self) -> float:
        prices = self.cart_info.locator(".inventory_item_price").all_text_contents()
        return sum([float(p.replace("$", "")) for p in prices])

    def click_checkout_button(self):
        self.checkout_button.click()
