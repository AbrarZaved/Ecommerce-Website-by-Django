from django.shortcuts import render

from product.models import Product

# Create your views here.

def product_details(request,slug):
    product=Product.objects.get(slug=slug)
    return render(request,'product/product_details.html',{"product":product})