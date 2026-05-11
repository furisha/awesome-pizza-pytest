from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """Menu section — browse pizzas and manage item quantities."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._menu = page.locator("#menu-container")

    def open(self):
        self.navigate("/")
        self._menu.locator(".menu-item").first.wait_for()

    def get_menu_item_names(self) -> list[str]:
        return self._menu.locator("h3").all_text_contents()

    def add_item(self, item_name: str, times: int = 1):
        plus_btn = self._menu.locator(f".menu-item:has(h3:text('{item_name}')) .quantity-btn").nth(1)
        for _ in range(times):
            plus_btn.click()

    def decrement_item(self, item_name: str):
        minus_btn = self._menu.locator(f".menu-item:has(h3:text('{item_name}')) .quantity-btn").nth(0)
        minus_btn.click()

    def get_item_quantity(self, item_name: str) -> int:
        qty = self._menu.locator(f".menu-item:has(h3:text('{item_name}')) .quantity-display").text_content()
        return int(qty)
