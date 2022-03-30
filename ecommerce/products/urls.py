from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.ProductViewSet, basename="products")

urlpatterns = router.urls
