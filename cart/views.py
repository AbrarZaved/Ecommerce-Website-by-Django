from django.shortcuts import redirect, render

from cart.models import Cart
from product.models import Product
from django.contrib import messages

# Create your views here.


def view_cart(request):
    return render(request, "cart/cart.html")


def add_cart(request, slug):
    product = Product.objects.get(slug=slug)
    cart = Cart.objects.create(
        user=request.user, product=product, selling_price=product.price
    )
    messages.success(request, f"{product} added to cart")
    cart.save()
    return redirect("index")
