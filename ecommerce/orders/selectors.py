from typing import Optional

from django.shortcuts import get_object_or_404

from . import models


def order_get(id: str) -> Optional[models.Order]:
    """
    Returns an order.
    """
    return get_object_or_404(models.Order, id=id)
