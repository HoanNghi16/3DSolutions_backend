from django.contrib.auth.views import LoginView
from django.urls import path, include
from .views import RegistraionView
from .views import LoginView

urlpatterns = [
    path('register/', RegistraionView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]