from django.contrib import admin


from cart.models import Cart, Coupon, Memo, OrderHistory

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
    list_display = ["user", "display_users", "total_price", "coupon", "total_discount", "created_at"]  
    search_fields = ["cart__user__username", "cart__user__phone_number"]

    def display_users(self, obj):
        return ", ".join([str(cart.user) for cart in obj.cart.all()])

    display_users.short_description = "Cart Name"


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "quantity", "price", "created_at"]
    search_fields = ["user__username", "product__pid"]
    list_filter = ["user"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-created_at")