from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import models, serializers
from .services import product_delete, stock_update


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, pk):
        product_delete(pk)
        return Response(status=204)

    @action(detail=True, methods=["put"], url_path="stock-update")
    def update_stock(self, request, pk):
        serializer = serializers.ProductUpdateStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = stock_update(
            pk, serializer.validated_data["stock"], validate=False, replace=True
        )
        return Response(self.get_serializer(product).data, status=200)

    @action(detail=True, methods=["get"])
    def test(self, request, pk=None):
        return Response({"message": "test"}, status=200)
