from rest_framework import routers
from .viewsets import OrderViewSet

app_name = "order"

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename="order")

urlpatterns = router.urls
