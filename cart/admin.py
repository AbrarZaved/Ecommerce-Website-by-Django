from django.contrib import admin

from cart.models import Cart

# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user','product','selling_price','discount_price']
    list_filter=['user']
    search_fields=['user','product__pid']