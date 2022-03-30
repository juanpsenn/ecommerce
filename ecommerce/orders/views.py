from rest_framework import permissions, viewsets
from rest_framework.response import Response

from . import models, serializers
from .services import order_create


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_create(**serializer.validated_data)
        return Response(self.get_serializer(order).data, 201)
