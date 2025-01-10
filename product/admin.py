from django.contrib import admin

from product.models import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pid", "title", "category", "price"]
    list_filter = ["category", "sub_category"]
    search_fields = ["pid", "title"]

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-price")
