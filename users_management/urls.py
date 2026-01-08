from django.urls import path
from .views import RegistrationView, LoginView, UserInformationView, LogoutView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserInformationView.as_view(), name='info'),
    path('logout/', LogoutView.as_view(), name='logout'),
]