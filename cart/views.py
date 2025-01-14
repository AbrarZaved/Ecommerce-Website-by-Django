from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from cart.models import Cart
from product.models import Product
from django.contrib import messages

# Create your views here.


def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    return render(request, "cart/cart.html", {"carts": carts})


def add_cart(request, slug=None):
    if slug:
        product = Product.objects.get(slug=slug)
        if Cart.objects.filter(product__slug=slug).exists():
            return JsonResponse(
                {"success": False, "id": product.id, "product_name": product.title},
                safe=False,
            )
        else:
            Cart.objects.create(
                user=request.user, product=product, selling_price=product.price
            )
            return JsonResponse(
                {"success": True, "id": product.id, "product_name": product.title},
                safe=False,
            )

    data = json.loads(request.body)
    slug = data.get("cart_value")
    selling_price = data.get("newPrice")
    size = data.get("size")
    quantity = data.get("quantity")

    if not all([slug, selling_price, size, quantity]):
        return JsonResponse({"message": "Invalid data provided"}, status=400)

    product = Product.objects.get(slug=slug)
    cart_product = Cart.objects.filter(product__slug=slug)

    if cart_product.exists():
        cart_product.update(
            user=request.user,
            selling_price=selling_price,
            size=size,
            quantity=quantity,
        )
        return JsonResponse(
            {"success": False, "id": product.id, "product_name": product.title},
            safe=False,
        )

    Cart.objects.create(
        user=request.user,
        product=product,
        selling_price=selling_price,
        size=size,
        quantity=quantity,
    )
    return JsonResponse(
        {"success": True, "id": product.id, "product_name": product.title}, safe=False
    )


def delete_cart_item(request, boom):
    item = Cart.objects.get(pk=boom)
    item.delete()
    return redirect("cart")
