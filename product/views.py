from re import sub
from django.shortcuts import render

from product.models import Product

# Create your views here.

def product_details(request,slug):
    product=Product.objects.get(slug=slug)
    related_products=Product.objects.filter(sub_category=product.sub_category).exclude(slug=slug).order_by("-rating")[:10]
    sub_category=product.sub_category
    return render(request,'product/product_details.html',{"product":product,"related_products":related_products,"sub_category":sub_category})   