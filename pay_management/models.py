import uuid

from django.db import models

from orders_management.models import OrderHeaders


# Create your models here.
class OrderPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    pay_status = models.BooleanField(default=False)
