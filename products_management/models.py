import uuid
from django.db import models

class Materials(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    unit_price = models.FloatField()

    def __str__(self):
        return str({'id': self.id, 'name': self.name, 'description': self.description,'unit_price':  self.unit_price})
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit_price = models.FloatField()
    quantity = models.PositiveIntegerField()
    material = models.ForeignKey(Materials, related_name='products_material', on_delete=models.CASCADE)

    def __str__(self):
        return str({ id : self.id,'name' : self.name, 'description': self.description, 'unit_price': self.unit_price})

class ProductImages(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    fileID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    path = models.CharField(unique=True)
    is_thumbnail = models.BooleanField(default=False)
    type = models.CharField(max_length=100)
