from django.urls import path

from services_management.views import FileUploadView

urlpatterns = [
    path('file_upload/', FileUploadView.as_view(), name='file_upload'),
]