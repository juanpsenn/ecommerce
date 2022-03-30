from dataclasses import dataclass
from typing import List

from products.models import Product


@dataclass
class Item:
    product: Product
    quantity: int


def check_unique_products(items: List[dict]) -> bool:
    """
    Check if all products in the order are unique.
    """
    products = [i.product for i in items]
    return len(products) == len(set(products))
