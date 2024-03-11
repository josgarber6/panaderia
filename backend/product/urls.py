from django.urls import path
from . import views
from rest_framework import routers
from .viewsets import ProductViewSet, CategoryViewSet

app_name = "product"

# urlpatterns = [
#     path('<int:id>/', views.product_detail, name='product_detail'),
#     path('', views.catalogue, name='catalogue'),
#     path('<int:id>/publishOpinion/', views.publish_opinion, name='publish_opinion'),
#     path("search/", views.search_products, name="search_products"),
# ]

router = routers.SimpleRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = router.urls
