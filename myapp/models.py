from email.mime import image
from msilib.schema import Class
from django.db import models

# Create your models here.

class FactoryName(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)

class ProductName(models.Model):
    productsName=models.CharField(max_length=100)
    quantity=models.IntegerField()
    description=models.TextField(max_length=100)
    image = models.ImageField(
        max_length=None,default=1
    )
    factoryName=models.ForeignKey(FactoryName,on_delete=models.CASCADE)