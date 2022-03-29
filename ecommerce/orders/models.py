from django.db import models


class Order(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    date_time = models.DateTimeField(auto_now_add=True)


class OrderDetail(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.PROTECT)
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.IntegerField()
