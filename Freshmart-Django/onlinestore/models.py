from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# Create your models here.




class Products(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    sale_price = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=1000, blank=True, null=True)
    inventory = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=1000, blank=True, null=True)


    def __str__(self) -> str:
        return self.name
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.order} - {self.product}"
    

    
class CompletedOrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return f"{self.order} - {self.product}"


    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    Middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.comment

class SellOnFreshMart(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    email = models.EmailField(max_length=500,blank=True, null=True )
    subject = models.CharField(max_length=500, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.subject:  
            self.subject = self.email  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject







    
    





