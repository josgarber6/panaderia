from django.urls import path
from . import views
from rest_framework import routers
from .viewsets import CustomerViewSet

urlpatterns = [
  path('signup/', views.signup_view, name='signup'),
  path('signup/done', views.SignupCompleteView.as_view(), name='signup_complete'),
  path('logout/', views.logout_view, name='logout'),
  path('change-password/', views.change_password_view, name='change_password'),
  path('change-password/done/', views.change_password_done_view, name='change_password_done'),
  path('get-username-from-session/', views.get_username_from_session, name='get-username-from-session'),
]

router = routers.SimpleRouter()
router.register('customers', CustomerViewSet)
urlpatterns += router.urls
