from collections import OrderedDict
from typing import List, Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from products.services import stock_update

from . import models, selectors, serializers
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


def order_update(*, items: List[OrderedDict], order: str) -> Optional[models.Order]:
    """
    Validates and updates an order. If the order is invalid,
    raises ValidationError.

    :param: order: The order id.
    :param: items: A list of items.
    """
    items = [Item(**item) for item in items]
    order = selectors.order_get(order)

    if not check_unique_products(items):
        raise ValidationError("All products must be unique.")

    with transaction.atomic():
        order_details_update(order, items)
    return order


def order_details_update(order: models.Order, items: List[Item]):
    order_items = order.items.select_related("product").all()

    # Update existing items
    for item in items:
        order_item = order_items.filter(product=item.product, order=order).first()
        if order_item:
            old_quantity = order_item.quantity
            order_item.quantity = item.quantity
            order_item.save()
            stock_update(item.product, (old_quantity - item.quantity))
        else:
            models.OrderDetail.objects.create(
                order=order, product=item.product, quantity=item.quantity
            )
            stock_update(item.product, -item.quantity)

    # Delete removed items
    drop_deleted_items(order, items)


def drop_deleted_items(order: models.Order, items: List[Item]):
    # TODO: maybe should be handled by a signal?
    products = [item.product for item in items]
    deleted_items = order.items.select_related("product").exclude(product__in=products)

    for item in deleted_items:
        stock_update(item.product, item.quantity)
        item.delete()


def order_delete(*, order: str) -> Optional[OrderedDict]:
    """
    Deletes an order and its details. Also restores
    the stock of the products.

    :param: order: The order id.
    """
    order = selectors.order_get(order)
    order_data = serializers.OrderSerializer(order).data

    with transaction.atomic():
        order_details_delete(order)
        order.delete()
    return order_data


def order_details_delete(order: models.Order):
    order_items = order.items.select_related("product").all()

    for item in order_items:
        stock_update(item.product, item.quantity)
        item.delete()
