from django.urls import path
from .views import RegistrationView, LoginView, UserInformationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('info/<uuid:user_id>/', UserInformationView.as_view(), name='info'),
]