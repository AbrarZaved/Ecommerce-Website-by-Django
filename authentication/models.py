from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.


class Customer(AbstractBaseUser):

    male = "male"
    female = "female"
    other = "other"
    GENDER = [(male, "Male"), (female, "Female"), (other, "Other")]

    home = "home"
    office = "office"
    ADDRESS = [(home, "Home"), (office, "Office")]

    name = models.CharField(max_length=70, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=50, choices=GENDER)
    address = models.CharField(max_length=50, choices=ADDRESS)
    shipping_address = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups=None
    user_permission=None
