from typing import Union

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from . import models
from .selectors import product_get


def stock_update(product: Union[models.Product, str], quantity: int):
    """
    Update the stock of a product if has enought stock.
    Otherwise, raise ValidationError.
    """
    if not isinstance(product, models.Product):
        product = product_get(product)
    product.stock += quantity

    if product.stock < 0:
        raise ValidationError(f"Product {product.name} has no stock left.")

    product.save()


def product_delete(product: str):
    """
    Delete a product.

    :param: product: Product id to delete.
    """
    product = product_get(product)
    try:
        product.delete()
    except IntegrityError:
        raise ValidationError(f"Product {product.name} has orders.")
