from rest_framework import serializers

from . import models


class OrderDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = models.OrderDetail
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, allow_empty=False)
    total = serializers.SerializerMethodField(read_only=True)

    def get_total(self, order):
        if self.context.get("currency") == "USD":
            return round(order.get_total_usd, 2)
        return round(order.get_total, 2)

    class Meta:
        model = models.Order
        fields = ["id", "date_time", "items", "total"]


class OrderUpdateSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, allow_empty=False)

    class Meta:
        model = models.Order
        exclude = ["id"]
