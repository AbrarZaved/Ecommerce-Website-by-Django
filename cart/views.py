from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import json
from django.contrib.auth.decorators import login_required
from authentication.models import Addressbook
from cart.models import Cart, Coupon, Memo, OrderHistory
from product.models import Product
from pytz import timezone
import datetime

# Create your views here.


@login_required(login_url="/index")
def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    addresses = Addressbook.objects.filter(user=request.user).order_by("-is_default")
    total_price = carts.aggregate(total=Sum("selling_price"))["total"] or 0
    Memo.objects.filter(user=request.user).update(coupon=None)
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
    messages.info(request, "Item Removed from Cart")
    return redirect("cart")


def update_cart(request):
    data = json.loads(request.body)
    slug = data.get("productName")
    size = data.get("size")
    quantity = data.get("quantity")
    price = data.get("newPrice")
    discount_price = data.get("discount_price") if quantity >= 3 else 0
    print(slug, size, quantity, price, discount_price)
    cart_product = Cart.objects.get(product__slug=slug, user=request.user)
    cart_product.size = size
    cart_product.quantity = quantity
    cart_product.selling_price = price
    cart_product.discount_price = discount_price
    cart_product.save()

    total_price = Cart.objects.filter(user=request.user).aggregate(
        total=Sum("selling_price")
    )["total"]
    return JsonResponse({"success": True, "total_price": total_price}, safe=False)


def coupon_handle(request):
    if request.method != "POST":
        return
    data = json.loads(request.body)
    coupon_name = data.get("coupon_name", "").upper()

    # Get the total selling price from the cart
    sub_total = (
        Cart.objects.filter(user=request.user).aggregate(total=Sum("selling_price"))[
            "total"
        ]
        or 0
    )

    # Get the coupon if it exists
    coupon = Coupon.objects.filter(coupon_name=coupon_name).first()

    discount_price = coupon.discount_price if coupon else 0

    memo, created = Memo.objects.get_or_create(user=request.user)

    if coupon:
        memo.coupon = coupon
        memo.total_discount = memo.total_discount + discount_price
        memo.total_price = memo.total_price - discount_price
    else:
        # Reset total_price and total_discount if the coupon is invalid
        memo.total_price = sub_total
        memo.total_discount = (
            Cart.objects.filter(user=request.user).aggregate(
                discount=Sum("discount_price")
            )["discount"]
            or 0
        )
        memo.coupon = None

    memo.save()

    return JsonResponse(
        {
            "discount_price": discount_price,
            "sub_total": sub_total,
            "total_price": memo.total_price,
            "total_discount": memo.total_discount,
        },
        safe=False,
    )


def handle_cart_update(
    request, slug, selling_price=None, size="S", quantity=1, single=False
):
    product = Product.objects.get(slug=slug)
    if cart_product := Cart.objects.filter(product=product, user=request.user).first():
        # Update fields directly on the instance
        cart_product.selling_price = selling_price or product.price
        cart_product.size = size
        cart_product.quantity = quantity
        cart_product.save()

        response = {
            "success": False,
            "id": product.id,
            "product_name": product.title,
        }
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            selling_price=(selling_price or product.price),
            size=size,
            quantity=quantity,
        )
        total_item = Cart.objects.filter(user=request.user).count()
        response = {
            "success": True,  # Indicates a new entry was created
            "id": product.id,
            "product_name": product.title,
            "total_item": total_item,
        }

    return JsonResponse(response, safe=False)


def checkout(request):
    memo = Memo.objects.filter(user=request.user).values_list(
        "cart__product__title",
        "cart__size",
        "cart__quantity",
        "cart__selling_price",
        "cart__discount_price",
    )
    created_at = Memo.objects.get(user=request.user).created_at
    dhaka_tz = timezone("Asia/Dhaka")
    created_at = created_at.astimezone(dhaka_tz).strftime("%Y-%m-%d %I:%M:%S %p")
    total_discount = Memo.objects.get(user=request.user).total_discount
    total_price = Memo.objects.get(user=request.user).total_price
    coupon = (
        Memo.objects.get(user=request.user).coupon.coupon_name
        if Memo.objects.get(user=request.user).coupon
        else None
    )
    user_name = request.user.name
    user_phone_number = request.user.phone_number
    user_email = request.user.email
    user_address = request.user.default_address.address
    items = [
        total_discount,
        total_price,
        coupon,
        user_name,
        user_phone_number,
        user_email,
        user_address,
        created_at,
    ]
    memo = list(memo)
    memo.append(items)
    products = list(
        Memo.objects.get(user=request.user)
        .cart.all()
        .values("product__id", "selling_price", "quantity")
    )
    for product in products:
        OrderHistory.objects.create(
            user=request.user,
            product=Product.objects.get(id=product["product__id"]),
            quantity=product["quantity"],
            price=product["selling_price"],
        )
    Cart.objects.filter(user=request.user).delete()
    return JsonResponse(memo, safe=False)
