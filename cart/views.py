from django.db.models import F, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from authentication.models import Addressbook
from cart.models import Cart, Coupon, Memo
from product.models import Product

# Create your views here.


def view_cart(request):
    carts = Cart.objects.filter(user=request.user)
    addresses = Addressbook.objects.filter(user=request.user).order_by("-is_default")
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
    if request.method == "POST":
        data = json.loads(request.body)
        coupon_name = data.get("coupon_name", "").upper()

        # Get the total selling price from the cart
        sub_total = (
            Cart.objects.filter(user=request.user).aggregate(
                total=Sum("selling_price")
            )["total"]
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
    cart_product = Cart.objects.filter(
        product=product, user=request.user
    ).first()  # Get the first matching cart

    if cart_product:
        # Update fields directly on the instance
        cart_product.selling_price = (selling_price or product.price) * quantity
        cart_product.size = size
        cart_product.quantity = quantity
        cart_product.save()  # Save the instance to trigger the post_save signal

        response = {
            "success": False,  # Indicates update rather than create
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
            "success": True,  # Indicates a new entry was created
            "id": product.id,
            "product_name": product.title,
        }

    return JsonResponse(response, safe=False)


def checkout(request):
    if request.method == "POST":
        user = request.user
        queryset = Memo.objects.filter(user=user)
        for obj in queryset:
            total_price = obj.total_price
            total_discount = obj.total_discount
            coupon = obj.coupon
        # Create PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="cash_memo.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Cash Memo")

        # Title in large text
        pdf.setFont("Times-Bold", 24)
        pdf.drawCentredString(300, 770, "GOLPO GHOR")

        pdf.setFont("Times-Roman", 12)
        pdf.drawString(100, 750, "--------------------------------")

        y_position = 730

        if queryset.exists():
            first_obj = queryset.first()
            pdf.drawString(100, y_position, f"Name: {first_obj.user.name}")
            y_position -= 20
            pdf.drawString(
                100, y_position, f"Phone Number: {first_obj.user.phone_number}"
            )
            y_position -= 20
            pdf.drawString(
                100, y_position, f"Address: {first_obj.user.default_address.address}"
            )
            y_position -= 20

        pdf.drawString(100, y_position, "--------------------------------")
        y_position -= 20

        headers = ["Product", "Size", "Quantity", "Selling Price", "Discount Price"]
        data = [headers]
        sub_total = 0

        for obj in queryset:
            for cart in obj.cart.all():
                data_row = [
                    cart.product.title,
                    cart.size,
                    cart.quantity,
                    f"{cart.selling_price:.2f}",
                    f"{cart.discount_price:.2f}",
                ]
                data.append(data_row)

        table_y_position = y_position - len(data) * 20
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )

        table.wrapOn(pdf, 100, table_y_position)
        table.drawOn(pdf, 100, table_y_position)

        sub_total = total_price + total_discount
        y_offset = 40

        pdf.setFont("Times-Bold", 12)
        pdf.drawRightString(
            500, table_y_position - y_offset, f"Subtotal: {sub_total:.2f}"
        )
        y_offset += 20

        if coupon:
            pdf.drawRightString(
                500, table_y_position - y_offset, f"Coupon Used: {coupon}"
            )
            y_offset += 20

        pdf.drawRightString(
            500, table_y_position - y_offset, f"Total Discount: {total_discount:.2f}"
        )
        y_offset += 20

        pdf.drawRightString(
            500,
            table_y_position - y_offset,
            f"Total Amount To be Paid: {total_price:.2f}",
        )

        pdf.save()
        return response
