from dataclasses import dataclass


@dataclass
class AppTestData:
    customer_name: str
    order_item: str
    order_quantity: int
    invalid_order_id: str
