from django.contrib import admin
from django.contrib.auth.models import Group
from authentication.models import Customer

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone_number"]
    list_per_page = 100
    search_fields = ["name", "email", "phone_number"]


admin.site.unregister(Group)
