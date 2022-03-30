from rest_framework import serializers

from . import models


class OrderDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = models.OrderDetail
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, allow_empty=False)

    class Meta:
        model = models.Order
        fields = "__all__"


class OrderUpdateSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, allow_empty=False)

    class Meta:
        model = models.Order
        exclude = ["id"]
