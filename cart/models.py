from django.db import models

from authentication.models import Customer
from product.models import Product

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    selling_price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)


    def __str__(self):
        return str(self.user)