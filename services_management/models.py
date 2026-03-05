import uuid

from django.db import models

# Create your models here.
class CustomerUploaded(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_file_id = models.CharField(max_length=100, default="", null=True)
    path = models.CharField(max_length=200, default="")
    type = models.CharField(max_length=100, default="avt")
