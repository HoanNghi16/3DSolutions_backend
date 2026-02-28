import uuid

from django.db import models
from products_management.models import Products
from users_management.models import Users, Address


# Create your models here.
class OrderHeaders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    total = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    pay_status = models.IntegerField(default=0)
    method = models.IntegerField(default=0)
    order_status = models.IntegerField(default=0)
    receiver_phone = models.CharField(max_length=15, unique=False, null=True, default=None)
    receiver_name = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100, default='')
    ward = models.CharField(max_length=100, default='')
    street = models.CharField(max_length=100, default='')
    number = models.CharField(max_length=30, default="")
    expire_at = models.DateTimeField(null = True)

    def __str__(self):
        return f'id = {self.id}, user = {self.user}, total = {self.total}'
    def get_id(self):
        return self.id
class OrderDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    header = models.ForeignKey(OrderHeaders, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    current_price = models.FloatField( default=0)

    def __str__(self):
        return f'header_id: {self.header.id}, detail_id: {self.id}, product_id: {self.product.id}, quantity: {self.quantity}'