from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("cart", views.view_cart, name="cart"),
    path(
        "delete_cart_item/<slug:slug>", views.delete_cart_item, name="delete_cart_item"
    ),
    path("add_cart/<slug:slug>", csrf_exempt(views.add_cart), name="add_cart"),
    path("buy_now/<slug:slug>", csrf_exempt(views.buy_now), name="buy_now"),
    path("buy_now", csrf_exempt(views.buy_now), name="buy_now"),
    path("coupon_handle", csrf_exempt(views.coupon_handle), name="coupon_handle"),
    path("add_cart", csrf_exempt(views.add_cart), name="add_cart"),
    path("update_cart", csrf_exempt(views.update_cart), name="update_cart"),
]
