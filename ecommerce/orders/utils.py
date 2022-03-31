from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional

import requests
from products.models import Product

USD_API = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"


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


def get_usd_quote(name: str = "Dolar Blue") -> Optional[float]:
    """
    Get the USD quote from the API.
    """
    response = requests.get(USD_API)
    for usd in response.json():
        if usd["casa"]["nombre"] == name:
            return Decimal(usd["casa"]["venta"].replace(",", "."))
    raise ValueError(f"Cannot find {name} in the response.")
