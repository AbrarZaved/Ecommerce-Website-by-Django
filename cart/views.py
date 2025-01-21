from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import json

from authentication.models import Addressbook
from cart.models import Cart, Coupon
from product.models import Product

# Create your views here.


def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    addresses = Addressbook.objects.filter(user=request.user)
    total_price = carts.aggregate(total=Sum("selling_price"))["total"] or 0

    return render(
        request,
        "cart/cart.html",
        {
            "carts": carts,
            "addresses": addresses,
            "total_price": total_price,
        },
    )


def buy_now(request, slug=None):
    if slug:
        return handle_cart_update(request, slug, single=True)

    data = json.loads(request.body)
    slug = data.get("product_slug")
    selling_price = data.get("newPrice")
    size = data.get("size")
    quantity = data.get("quantity")

    return handle_cart_update(request, slug, selling_price, size, quantity)


def add_cart(request, slug=None):
    if slug:
        return handle_cart_update(request, slug)

    data = json.loads(request.body)
    slug = data.get("cart_value")
    selling_price = data.get("newPrice")
    size = data.get("size")
    quantity = data.get("quantity")

    if not all([slug, selling_price, size, quantity]):
        return JsonResponse({"message": "Invalid data provided"}, status=400)

    return handle_cart_update(request, slug, selling_price, size, quantity)


def delete_cart_item(request, slug):
    Cart.objects.filter(product__slug=slug).delete()
    messages.success(request, "Item Removed from Cart")
    return redirect("cart")


def update_cart(request):
    data = json.loads(request.body)
    slug = data.get("productName")
    size = data.get("size")
    quantity = data.get("quantity")
    price = data.get("newPrice")
    discount_price = data.get("discount_price") if quantity >= 3 else 0

    Cart.objects.filter(product__slug=slug).update(
        size=size, quantity=quantity, selling_price=price, discount_price=discount_price
    )

    total_price = Cart.objects.filter(user=request.user).aggregate(
        total=Sum("selling_price")
    )["total"]
    return JsonResponse({"success": True, "total_price": total_price}, safe=False)


def coupon_handle(request):
    if request.method == "POST":
        data = json.loads(request.body)
        coupon_name = data.get("coupon_name", "").upper()
        coupons = Coupon.objects.values_list("coupon_name", flat=True)
        sub_total = Cart.objects.filter(user=request.user).aggregate(
            total=Sum("selling_price")
        )["total"]

        discount_price = (
            Coupon.objects.filter(coupon_name=coupon_name).first().discount_price
            if coupon_name in coupons
            else 0
        )

        return JsonResponse(
            {"discount_price": discount_price, "sub_total": sub_total}, safe=False
        )


def handle_cart_update(
    request, slug, selling_price=None, size=None, quantity=1, single=False
):
    product = Product.objects.get(slug=slug)
    cart_product = Cart.objects.filter(product=product, user=request.user)

    if cart_product.exists():
        cart_product.update(
            selling_price=(selling_price or product.price) * quantity,
            size=size,
            quantity=quantity,
        )
        response = {
            "success": False,
            "id": product.id,
            "product_name": product.title,
        }
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            selling_price=(selling_price or product.price) * quantity,
            size=size,
            quantity=quantity,
        )

        response = {
            "success": True,
            "id": product.id,
            "product_name": product.title,
        }
    return JsonResponse(response, safe=False)
