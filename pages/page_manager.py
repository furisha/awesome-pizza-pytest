from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.order_page import OrderPage
from pages.navigation_page import NavigationPage


class PageManager:
    """Lazy-init factory for all page sections."""

    def __init__(self, page: Page):
        self._page = page
        self._home: HomePage | None = None
        self._order: OrderPage | None = None
        self._nav: NavigationPage | None = None

    @property
    def home(self) -> HomePage:
        if self._home is None:
            self._home = HomePage(self._page)
        return self._home

    @property
    def order(self) -> OrderPage:
        if self._order is None:
            self._order = OrderPage(self._page)
        return self._order

    @property
    def nav(self) -> NavigationPage:
        if self._nav is None:
            self._nav = NavigationPage(self._page)
        return self._nav
