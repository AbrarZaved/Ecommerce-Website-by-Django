from django.shortcuts import render

from product.models import Product

# Create your views here.

def product_details(request,boom):
    product=Product.objects.get(pk=boom)
    return render(request,'product/product_details.html',{"product":product})