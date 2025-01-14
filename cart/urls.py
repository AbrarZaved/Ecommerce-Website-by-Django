from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("cart", views.view_cart, name="cart"),
    path(
        "delete_cart_item/<int:boom>", views.delete_cart_item, name="delete_cart_item"
    ),
    path("add_cart/<slug:slug>", csrf_exempt(views.add_cart), name="add_cart"),
    path("add_cart", csrf_exempt(views.add_cart), name="add_cart"),
]
