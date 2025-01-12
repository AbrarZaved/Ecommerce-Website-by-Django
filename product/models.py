from django.db import models
from django.utils.text import slugify
import uuid

# Create your models here.


class Product(models.Model):
    pid = models.CharField(max_length=50, unique=True, null=False, blank=False)
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    category = models.CharField(max_length=150, null=False, blank=False)
    sub_category = models.CharField(max_length=150, null=False, blank=False)
    brand = models.CharField(max_length=110)
    price = models.IntegerField(default=0)
    images = models.TextField()
    product_details = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    out_of_stock = models.BooleanField(default=False)
    seller = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=200, null=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
            self.slug = unique_slug
        super().save(*args, **kwargs)
