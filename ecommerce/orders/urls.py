from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("", views.OrderViewSet, basename="orders")

urlpatterns = router.urls
