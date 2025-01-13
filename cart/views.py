from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from cart.models import Cart
from product.models import Product
from django.contrib import messages

# Create your views here.


def view_cart(request):
    return render(request, "cart/cart.html")


def add_cart(request):
    slug = json.loads(request.body).get("cart_value")
    product = Product.objects.get(slug=slug)
    if Cart.objects.filter(product__slug=slug).exists():
        return JsonResponse(
            {"success": False, "id": product.id, "product_name": product.title},
            safe=False,
        )
    cart = Cart.objects.create(
        user=request.user, product=product, selling_price=product.price
    )
    cart.save()
    return JsonResponse({"success": True,"id":product.id,"product_name":product.title}, safe=False)
