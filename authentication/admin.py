from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.models import Addressbook, Customer

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone_number"]
    list_per_page = 100
    search_fields = ["name", "email", "phone_number"]


admin.site.unregister(Group)


@admin.register(Addressbook)
class AdressbookAdmin(admin.ModelAdmin):
    list_display = ["user", "address_label", "division", "city"]
    list_per_page = 100
    search_fields = ["user", "user__phone_number"]
    list_filter = ["address_label", "division", "city", "zone"]
