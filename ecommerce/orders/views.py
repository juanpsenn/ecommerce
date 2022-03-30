from rest_framework import permissions, viewsets
from rest_framework.response import Response

from . import models, serializers
from .services import order_create, order_delete, order_update


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_create(**serializer.validated_data)
        return Response(self.get_serializer(order).data, 201)

    def update(self, request, pk):
        serializer = serializers.OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_update(**serializer.validated_data, order=pk)
        return Response(self.get_serializer(order).data, 201)

    def destroy(self, request, pk):
        order = order_delete(order=pk)
        return Response(order, 200)
