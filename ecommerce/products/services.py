from typing import Union

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from . import models
from .selectors import product_get


def stock_update(
    product: Union[models.Product, str],
    quantity: int = 0,
    validate: bool = True,
    replace: bool = True,
):
    """
    Update the stock of a product if has enought stock.
    Otherwise, raise ValidationError.

    :param: product: Product id or object to update.
    :param: quantity: Quantity to update.
    :param: validate: If True, validate the stock is >0.
    :param: replace: If True, replace the stock, otherwise, add the quantity.
    """
    if not isinstance(product, models.Product):
        product = product_get(product)

    if not replace:
        product.stock += quantity
    else:
        product.stock = quantity

    if product.stock < 0 and validate:
        raise ValidationError(f"Product {product.name} has no stock left.")

    product.save()
    return product


def product_delete(product: str):
    """
    Delete a product. Prevent deleting a product with orders.

    :param: product: Product id to delete.
    """
    product = product_get(product)
    try:
        product.delete()
    except IntegrityError:
        raise ValidationError(f"Product {product.name} has orders.")
