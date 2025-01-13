from django.urls import path
from . import views


urlpatterns = [
    path("cart", views.view_cart, name="cart"),
    path("add_cart/<slug:slug>", views.add_cart, name="add_cart"),
]
