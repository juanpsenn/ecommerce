from django.core.exceptions import ValidationError

from . import models


def stock_update(product: models.Product, quantity: int):
    """
    Update the stock of a product if has enought stock.
    Otherwise, raise ValidationError.
    """
    product.stock += quantity

    if product.stock < 0:
        raise ValidationError(f"Product {product.name} has no stock left.")

    product.save()
