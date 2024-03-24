from rest_framework import routers
from .viewsets import ProductViewSet, CategoryViewSet

app_name = "product"

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = router.urls
