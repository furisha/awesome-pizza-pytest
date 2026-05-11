from pages.page_manager import PageManager
from models.pizza import AppTestData


class TestMenu:
    def test_menu_displays_all_items(self, page_manager: PageManager, api_menu_items: list[str]):
        page_manager.home.open()
        assert page_manager.home.get_menu_item_names() == api_menu_items


class TestCart:
    def test_place_order_button_disabled_by_default(self, page_manager: PageManager):
        page_manager.home.open()
        assert not page_manager.order.is_place_order_enabled()

    def test_add_item_increments_cart_total(self, page_manager: PageManager, test_data: AppTestData):
        page_manager.home.open()
        page_manager.home.add_item(test_data.order_item)
        assert page_manager.order.get_cart_total() == 1

    def test_remove_item_shows_empty_cart(self, page_manager: PageManager, test_data: AppTestData):
        page_manager.home.open()
        page_manager.home.add_item(test_data.order_item)
        page_manager.order.remove_from_cart(test_data.order_item)
        assert page_manager.order.is_cart_empty()

    def test_quantity_increment_and_decrement(self, page_manager: PageManager, test_data: AppTestData):
        page_manager.home.open()
        page_manager.home.add_item(test_data.order_item, times=3)
        page_manager.home.decrement_item(test_data.order_item)
        assert page_manager.home.get_item_quantity(test_data.order_item) == 2


class TestOrderPlacement:
    def test_place_order_shows_success_notification(
        self, page_manager: PageManager, test_data: AppTestData
    ):
        page_manager.home.open()
        page_manager.order.set_customer_name(test_data.customer_name)
        page_manager.home.add_item(test_data.order_item)
        page_manager.order.place_order()
        notification = page_manager.nav.get_notification_text()
        assert "Order placed successfully" in notification
        assert "Order ID:" in notification


class TestOrderLookup:
    def test_lookup_order_after_placing(self, page_manager: PageManager, test_data: AppTestData):
        page_manager.home.open()
        page_manager.order.set_customer_name(test_data.customer_name)
        page_manager.home.add_item(test_data.order_item)
        page_manager.order.place_order()
        page_manager.nav.get_notification_text()  # wait for order to complete
        order_id = page_manager.order.get_prefilled_order_id()
        page_manager.order.lookup_order(order_id)
        assert page_manager.order.is_order_details_visible()
        assert test_data.customer_name in page_manager.order.get_order_customer()

    def test_lookup_invalid_order_id_shows_error(
        self, page_manager: PageManager, test_data: AppTestData
    ):
        page_manager.home.open()
        page_manager.order.lookup_order(test_data.invalid_order_id)
        notification = page_manager.nav.get_notification_text()
        assert "not found" in notification.lower() or "error" in notification.lower()


class TestOrderStatusTransitions:
    def test_order_progresses_received_to_delivered(
        self, page_manager: PageManager, test_data: AppTestData
    ):
        page_manager.home.open()
        page_manager.order.set_customer_name(test_data.customer_name)
        page_manager.home.add_item(test_data.order_item)
        page_manager.order.place_order()
        page_manager.nav.get_notification_text()
        order_id = page_manager.order.get_prefilled_order_id()
        page_manager.order.lookup_order(order_id)
        assert page_manager.order.get_order_status() == "RECEIVED"
        page_manager.order.mark_as_delivering()
        assert page_manager.order.get_order_status() == "DELIVERING"
        page_manager.order.mark_as_delivered()
        assert page_manager.order.get_order_status() == "DELIVERED"


class TestTheme:
    def test_theme_toggle_switches_between_dark_and_light(self, page_manager: PageManager):
        page_manager.home.open()
        assert not page_manager.nav.is_dark_mode()
        page_manager.nav.toggle_theme()
        assert page_manager.nav.is_dark_mode()
        page_manager.nav.toggle_theme()
        assert not page_manager.nav.is_dark_mode()
