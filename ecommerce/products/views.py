from rest_framework import permissions, viewsets
from rest_framework.response import Response

from . import models, serializers
from .services import product_delete


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, pk):
        product_delete(pk)
        return Response(status=204)
