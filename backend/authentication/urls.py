from django.urls import path
from . import views

urlpatterns = [
  path('signup/', views.signup_view, name='signup'),
  path('signup/done', views.SignupCompleteView.as_view(), name='signup_complete'),
  path('logout/', views.logout_view, name='logout'),
  path('change_password/', views.change_password_view, name='change_password'),
  # path('get-username-from-session/', views.get_username_from_session, name='get-username-from-session'),
]

