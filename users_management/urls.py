from django.urls import path
from .views import RegistrationView, LoginView, UserInformationView, LogoutView, NewAddressView, UsersAdminView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserInformationView.as_view(), name='info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('address/', NewAddressView.as_view(), name='address'),
    path('admin_users/', UsersAdminView.as_view(), name='admin_users'),
]