from django.contrib import admin

from cart.models import Cart, Coupon, Memo

# Register your models here.


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
        "size",
        "quantity",
        "selling_price",
        "discount_price",
    ]
    list_filter = ["user"]
    search_fields = ["user", "product__pid"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-created_at")


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["coupon_name", "discount_price"]
    search_fields = ["coupon_name"]


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ["cart__user", "coupon__coupon_name"]
    search_fields = ["cart__user", "cart_user__phone_number"]
