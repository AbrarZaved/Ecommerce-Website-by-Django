from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import Customer
from product.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, default="S")
    selling_price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

