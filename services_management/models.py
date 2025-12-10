import uuid

from django.db import models

from products_management.models import Materials
from users_management.models import UserAccounts


# Create your models here.
class Services(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()

class ServiceOrderHeaders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateField()

class ServiceOrderDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    header = models.ForeignKey(ServiceOrderHeaders, on_delete=models.CASCADE)
    cus_description = models.TextField()
    material = models.ForeignKey(Materials, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(null = True)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)

class CustomerUploaded(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.ForeignKey(ServiceOrderDetails, on_delete=models.CASCADE)
    path = models.FilePathField()
    type = models.CharField(max_length=10)
