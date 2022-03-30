from . import models


def stock_update(product: models.Product, quantity: int):
    """
    Update the stock of a product.
    """
    product.stock += quantity
    product.save()
