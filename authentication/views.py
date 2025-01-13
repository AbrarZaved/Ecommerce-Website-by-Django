from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import json
from django.contrib import messages
from authentication.forms import AddressForm, CustomerForm
from authentication.models import Addressbook, Customer

# Django View
from django.http import JsonResponse


def sign_in(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("loginPhone")
        password = data.get("loginPassword")

        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                {
                    "success": True,
                    "toast_message": "Successfully Logged in",
                    "redirect_url": "/index",
                }
            )
        else:
            return JsonResponse(
                {"success": False, "toast_message": "Invalid credentials"}
            )


def sign_up(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("registerPhone")
        password = data.get("registerPassword")
        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.success(request, "Phone Number is Already Registered")
            return redirect("index")
        user = Customer.objects.create_user(
            phone_number=phone_number, password=password
        )
        user.save()
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            messages.info(
                request, "Registration Successful, Please Complete your profile"
            )
            return redirect("index")


def sign_out(request):
    logout(request)
    messages.success(request, "Log Out Successful")
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
            messages.success(request, "Address Added")
            return redirect("profile")

        if profile.is_valid():
            profile.save()
            messages.info(request, "Profile Updated")
            return redirect("profile")

    return redirect("profile")


def delete_address(request, boom):
    address = Addressbook.objects.get(pk=boom)
    address.delete()
    messages.success(request, "Address Deleted")
    return redirect("profile")


def edit_address(request, boom):
    if request.method == "POST":
        address_label = request.POST.get("address_label")
        address = request.POST.get("address")
        city = request.POST.get("city")
        division = request.POST.get("division")
        zone = request.POST.get("zone")

        address_instance = Addressbook.objects.get(pk=boom)
        address_instance.address_label = address_label
        address_instance.address = address
        address_instance.city = city
        address_instance.division = division
        address_instance.zone = zone
        address_instance.save()
        messages.info(request, "Address Updated")
        return redirect("profile")

    return redirect("profile")


def default_address_handle(request, boom):
    address = Addressbook.objects.get(pk=boom)
    address.is_default = True
    Customer.objects.filter(id=request.user.id).update(default_address=address)
    address.save()
    messages.success(request, "Default Address Changed")
    return redirect("profile")
