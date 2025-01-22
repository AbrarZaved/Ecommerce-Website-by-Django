from ast import Add
from random import choice
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from fontTools.merge.unicode import is_Default_Ignorable

# Create your models here.


class CustomerManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone Number is Must")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_admin"):
            raise ValueError("Superuser must have is_admin=True.")
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)

    def get_by_natural_key(self, phone_number):
        return self.get(phone_number=phone_number)


class Customer(AbstractBaseUser):

    male = "male"
    female = "female"
    other = "other"
    GENDER = [(male, "Male"), (female, "Female"), (other, "Other")]

    name = models.CharField(max_length=70, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=False, blank=False)
    gender = models.CharField(max_length=50, choices=GENDER)
    default_address = models.ForeignKey(
        "authentication.Addressbook",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total_orders = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = None
    user_permission = None

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomerManager()

    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        """Check if the user has a specific permission."""
        return True

    def has_module_perms(self, app_label):
        """Check if the user has permissions to view the app `app_label`."""
        return True


class Addressbook(models.Model):

    home = "home"
    office = "office"

    ADDRESS = [(home, "Home"), (office, "Office")]

    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    division = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zone = models.CharField(max_length=100)
    address = models.TextField()
    address_label = models.CharField(max_length=50, choices=ADDRESS)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=Addressbook)
def post_save_receiver(sender, instance, created, **kwargs):
    if created and Addressbook.objects.filter(user=instance.user).count() == 1:
        # If this is the first Addressbook entry, set it as default
        instance.is_default = True
        instance.save()
        Customer.objects.filter(id=instance.user.id).update(default_address=instance)
    elif instance.is_default:
        # If an address is marked as default, unmark others
        Addressbook.objects.exclude(id=instance.id).update(is_default=False)
