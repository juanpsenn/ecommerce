from collections import OrderedDict
from typing import List, Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from products.services import stock_update

from . import models
from .utils import Item, check_unique_products


def order_create(*, id: str, items: List[OrderedDict]) -> Optional[models.Order]:
    """
    Validates and creates an order. If the order is invalid,
    raises ValidationError.

    :param: id: The order id.
    :param: items: A list of items.
    """
    items = [Item(**item) for item in items]

    if not check_unique_products(items):
        raise ValidationError("All products must be unique.")

    with transaction.atomic():
        order = models.Order.objects.create(id=id)
        order_details_create(order, items)
    return order


def order_details_create(order: models.Order, items: List[Item]):
    for item in items:
        models.OrderDetail.objects.create(
            order=order, product=item.product, quantity=item.quantity
        )
        stock_update(item.product, -item.quantity)
