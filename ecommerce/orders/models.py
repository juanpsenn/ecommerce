from django.db import models

from .utils import get_usd_quote


class Order(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return sum(item.get_subtotal for item in self.items.all())

    @property
    def get_total_usd(self):
        return self.get_total / get_usd_quote()


class OrderDetail(models.Model):
    order = models.ForeignKey(
        "orders.Order", on_delete=models.PROTECT, related_name="items"
    )
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.IntegerField()

    @property
    def get_subtotal(self):
        return self.product.price * self.quantity
