from playwright.sync_api import Page
from pages.base_page import BasePage


class NavigationPage(BasePage):
    """Header and global UI — theme toggle, notification banner."""

    def __init__(self, page: Page):
        super().__init__(page)
        self._theme_toggle = page.locator("#theme-toggle")
        self._notification = page.locator("#notification")

    def toggle_theme(self):
        self._theme_toggle.click()

    def is_dark_mode(self) -> bool:
        return self.page.locator("html").get_attribute("data-theme") == "dark"

    def get_notification_text(self) -> str:
        self._notification.wait_for(state="visible")
        return self._notification.text_content()
