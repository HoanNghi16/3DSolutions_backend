import uuid
from django.db import models
from products_management.models import Products
from users_management.models import UserAccounts


# Create your models here.
class CartHeaders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.OneToOneField(UserAccounts, on_delete=models.CASCADE)
    total = models.FloatField(default=0)

    def __str__(self):
        return f'header_id: {self.id}, account: {self.account.id}, total: {self.total}'



class CartDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    header = models.ForeignKey(CartHeaders, on_delete=models.CASCADE, related_name='cart_details')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'header_id: {self.header.id}, detail_id: {self.id}. product: {self.product.id}, quantity: {self.quantity}'