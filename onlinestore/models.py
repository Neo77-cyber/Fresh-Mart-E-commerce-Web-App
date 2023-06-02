from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    sale_price = models.IntegerField(blank=True, null=True)
    detail = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return str(self.product)


    

    
    
    

    
    





