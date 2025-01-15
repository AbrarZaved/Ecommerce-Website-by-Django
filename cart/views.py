from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from authentication.models import Addressbook
from cart.models import Cart
from product.models import Product
from django.contrib import messages

# Create your views here.


def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    addresses = Addressbook.objects.filter(user=request.user)
    return render(request, "cart/cart.html", {"carts": carts, "addresses": addresses})


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
            selling_price=(selling_price * quantity),
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
        selling_price=(selling_price * quantity),
        size=size,
        quantity=quantity,
    )
    return JsonResponse(
        {"success": True, "id": product.id, "product_name": product.title}, safe=False
    )


def delete_cart_item(request, boom):
    item = Cart.objects.get(pk=boom)
    item.delete()
    messages.success(request,"Item Removed from Cart")
    return redirect("cart")


def update_cart(request):
    data = json.loads(request.body)
    size = data.get("size")
    quantity = data.get("quantity")
    slug = data.get("productName")
    price = data.get("newPrice")
    print(price)
    discount_price = data.get("discount_price")
    cart_product = Cart.objects.filter(product__slug=slug)

    cart_product.update(
        size=size,
        quantity=quantity,
        selling_price=price,
        discount_price=discount_price if quantity >= 3 else 0,
    )
    total_price = Cart.objects.filter(user=request.user).aggregate(
        total=Sum("selling_price")
    )["total"]

    return JsonResponse({"success": True, "total_price": total_price}, safe=False)
