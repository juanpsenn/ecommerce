from typing import Optional

from django.shortcuts import get_object_or_404

from . import models


def product_get(id: str) -> Optional[models.Product]:
    """
    Returns a product.
    """
    return get_object_or_404(models.Product, id=id)
