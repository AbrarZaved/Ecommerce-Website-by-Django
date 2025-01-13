from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("cart", views.view_cart, name="cart"),
    path("add_cart", csrf_exempt(views.add_cart), name="add_cart"),
]
