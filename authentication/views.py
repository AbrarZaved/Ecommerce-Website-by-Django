from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json

from authentication.forms import AddressForm, CustomerForm
from authentication.models import Addressbook, Customer

# Create your views here.


def sign_in(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("loginPhone")
        password = data.get("loginPassword")

        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")


def sign_up(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("registerPhone")
        password = data.get("registerPassword")

        user = Customer.objects.create_user(
            phone_number=phone_number, password=password
        )
        user.save()
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")


def sign_out(request):
    logout(request)
    return redirect("index")


@login_required
def profile_view(request):
    user = request.user
    profile = CustomerForm(instance=user)
    address = AddressForm()
    addresses = Addressbook.objects.filter(user=request.user)
    return render(
        request,
        "authentication/profile.html",
        {"profile": profile, "address": address, "addresses": addresses},
    )


def profile_attributes(request):
    if request.method == "POST":
        profile = CustomerForm(request.POST, instance=request.user)
        address = AddressForm(request.POST)

        if address.is_valid():
            address_instance = address.save(commit=False)
            address_instance.user = request.user
            address_instance.save()
            return redirect("profile")

        if profile.is_valid():
            profile.save()
            return redirect("profile")

    return redirect("profile")

def delete_address(request,boom):
    address=Addressbook.objects.get(pk=boom)
    address.delete()
    return redirect('profile')