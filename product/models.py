from django.db import models

# Create your models here.


class Product(models.Model):
    pid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    category = models.CharField(max_length=150, null=False, blank=False)
    sub_category = models.CharField(max_length=150, null=False, blank=False)
    brand = models.CharField(max_length=110)
    price = models.IntegerField(default=0)
    images = models.ImageField(
        upload_to="Product_Image", height_field=None, width_field=None, max_length=None
    )
    product_details = models.CharField(max_length=500)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    out_of_stock = models.BooleanField(default=False)
    seller = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)