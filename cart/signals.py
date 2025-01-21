# cart/signals.py
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from numpy import rec
from openpyxl.styles.builtins import total
from .models import Cart, Memo


@receiver(post_save, sender=Cart)
def update_memo(sender, instance, **kwargs):
    # Get or create a Memo for the specific user
    memo, created = Memo.objects.get_or_create(user=instance.user)

    # Update the total price of the Memo
    cart_items = Cart.objects.filter(user=instance.user)
    total_price = cart_items.aggregate(total=models.Sum("selling_price"))["total"] or 0
    discount_price = cart_items.aggregate(total=models.Sum("discount_price"))["total"] or 0

    memo.total_discount = discount_price
    memo.total_price = total_price
    memo.cart.set(cart_items)
    memo.save()


@receiver(post_delete, sender=Cart)
def delete_memo(sender, instance, **kwargs):
    memo = Memo.objects.get(user=instance.user)
    total_price = memo.cart.aggregate(total=models.Sum("selling_price"))["total"] or 0
    discount_price = memo.cart.aggregate(total=models.Sum("discount_price"))["total"] or 0

    memo.total_discount = discount_price
    memo.total_price = total_price
    if memo.cart.count() == 0:
        memo.delete()
