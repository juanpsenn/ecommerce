from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers
from .selectors import order_get
from .services import order_create, order_delete, order_update


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def retrieve(self, request, pk):
        order = order_get(pk)
        return Response(
            self.get_serializer(order, context=request.query_params).data, 200
        )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_create(**serializer.validated_data)
        return Response(self.get_serializer(order).data, 201)

    def update(self, request, pk):
        serializer = serializers.OrderUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = order_update(**serializer.validated_data, order=pk)
        return Response(self.get_serializer(order).data, 200)

    def destroy(self, request, pk):
        order = order_delete(order=pk)
        return Response(order, 200)
