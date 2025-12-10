from django.contrib.auth.views import LoginView
from django.urls import path
from .views import RegistraionView,LoginView

urlpatterns = [
    path('register/', RegistraionView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]