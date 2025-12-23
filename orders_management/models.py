import uuid

from django.db import models
from products_management.models import Products
from users_management.models import Users


# Create your models here.
class OrderHeaders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    total = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id = {self.id}, user = {self.user}, total = {self.total}'
    def get_id(self):
        return self.id
class OrderDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    header = models.ForeignKey(OrderHeaders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'header_id: {self.header.id}, detail_id: {self.id}, product_id: {self.product.id}, quantity: {self.quantity}'