import json
import pytest
import requests
from pathlib import Path
from pages.page_manager import PageManager
from models.pizza import AppTestData


@pytest.fixture
def page_manager(page) -> PageManager:
    return PageManager(page)


@pytest.fixture(scope="session")
def test_data() -> AppTestData:
    data_path = Path(__file__).parent / "test_data" / "testdata.json"
    with open(data_path) as f:
        raw = json.load(f)
    return AppTestData(
        customer_name=raw["customer"]["name"],
        order_item=raw["order"]["item"],
        order_quantity=raw["order"]["quantity"],
        invalid_order_id=raw["invalid_order_id"],
    )


@pytest.fixture(scope="session")
def api_menu_items(pytestconfig) -> list[str]:
    base_url = pytestconfig.getini("base_url")
    response = requests.get(f"{base_url}/api/daily-menu")
    response.raise_for_status()
    data = response.json()
    return [item["name"] for item in data["data"]]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, pytestconfig):
    base_url = pytestconfig.getini("base_url")
    args = {**browser_context_args, "viewport": {"width": 1280, "height": 720}}
    if base_url:
        args["base_url"] = base_url
    return args
