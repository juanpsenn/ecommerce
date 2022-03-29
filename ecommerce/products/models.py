from django.db import models


class Product(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    stock = models.IntegerField(default=0)
