from rest_framework import routers
from .viewsets import OrderViewSet

app_name = "order"

router = routers.SimpleRouter()
router.register('orders', OrderViewSet)

urlpatterns = router.urls
