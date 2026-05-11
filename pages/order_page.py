from playwright.sync_api import Page
from pages.base_page import BasePage


class OrderPage(BasePage):
    """Cart, order placement, and order management section."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._name_input = page.locator("#customer-name")
        self._cart_items = page.locator("#cart-items")
        self._total_items = page.locator("#total-items")
        self._place_order_btn = page.locator("#place-order-btn")
        self._order_id_input = page.locator("#order-id")
        self._lookup_btn = page.locator("#lookup-order-btn")
        self._order_details = page.locator("#order-details")

    # --- Cart / order placement ---

    def set_customer_name(self, name: str):
        self._name_input.fill(name)

    def is_place_order_enabled(self) -> bool:
        return self._place_order_btn.is_enabled()

    def place_order(self):
        self._place_order_btn.click()

    def get_cart_total(self) -> int:
        return int(self._total_items.text_content())

    def is_cart_empty(self) -> bool:
        return self._cart_items.locator(".empty-cart").is_visible()

    def remove_from_cart(self, item_name: str):
        self._cart_items.locator(
            f".cart-item:has(.cart-item-name:text('{item_name}')) .remove-item-btn"
        ).click()

    # --- Order management ---

    def get_prefilled_order_id(self) -> str:
        return self._order_id_input.input_value()

    def lookup_order(self, order_id: str):
        self._order_id_input.fill(order_id)
        self._lookup_btn.click()

    def is_order_details_visible(self) -> bool:
        return self._order_details.is_visible()

    def get_order_status(self) -> str:
        return self._order_details.locator(".status-badge").text_content()

    def get_order_customer(self) -> str:
        return self._order_details.locator(
            ".order-info-item:has(.order-info-label:text('Customer')) .order-info-value"
        ).text_content()

    def mark_as_delivering(self):
        self._order_details.locator("button:has-text('Mark as Delivering')").click()
        self._order_details.locator(".status-badge", has_text="DELIVERING").wait_for()

    def mark_as_delivered(self):
        self._order_details.locator("button:has-text('Mark as Delivered')").click()
        self._order_details.locator(".status-badge", has_text="DELIVERED").wait_for()
