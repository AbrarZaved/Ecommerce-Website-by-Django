from django.contrib import admin

from product.models import Product, product_review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["pid", "title", "category", "price"]
    list_filter = ["category", "sub_category"]
    search_fields = ["pid", "title",'slug']

    def get_queryset(self, request):
        return super().get_queryset(request).order_by("-price")

@admin.register(product_review)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "user", "rating"]
    list_filter = ["rating"]
    search_fields = ["product__title", "user__email"]