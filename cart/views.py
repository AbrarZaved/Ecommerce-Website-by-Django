from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from authentication.models import Addressbook
from cart.models import Cart, Coupon
from product.models import Product
from django.contrib import messages

# Create your views here.


def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    addresses = Addressbook.objects.filter(user=request.user)
    total_price = Cart.objects.filter(user=request.user).aggregate(
        total=Sum("selling_price")
    )["total"]

    # Ensure total_price is not None
    total_price = total_price if total_price is not None else 0

    return render(
        request,
        "cart/cart.html",
        {"carts": carts, "addresses": addresses, "total_price": total_price},
    )


def buy_now(request, slug):

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


def delete_cart_item(request, slug):
    item = Cart.objects.get(product__slug=slug)
    item.delete()
    messages.success(request, "Item Removed from Cart")
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


def coupon_handle(request):
    if request.method == "POST":
        coupon_name = json.loads(request.body).get("coupon_name").upper()
        coupons = list(Coupon.objects.all().values_list("coupon_name", flat=True))
        sub_total = Cart.objects.filter(user=request.user).aggregate(
            total=Sum("selling_price")
        )["total"]
        discount_price = 0
        if coupon_name in coupons:
            discount_price = Coupon.objects.get(coupon_name=coupon_name).discount_price
            return JsonResponse(
                {"discount_price": discount_price, "sub_total": sub_total}, safe=False
            )
        else:
            return JsonResponse(
                {"discount_price": discount_price, "sub_total": sub_total}, safe=False
            )
