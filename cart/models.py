from django.db import models
from authentication.models import Customer
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, default="S")
    selling_price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        temp_selling_price = self.selling_price
        self.selling_price = self.selling_price * self.quantity
        if self.quantity >= 3:
            self.discount_price = self.quantity * 100
            self.selling_price = (
                temp_selling_price * self.quantity - self.discount_price
            )
        super().save(*args, **kwargs)


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=50)
    discount_price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.coupon_name)


class Memo(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)
    total_discount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        first_cart = self.cart.first()
        if first_cart and first_cart.user:
            return f"Memo for {first_cart.user}"
        return "Memo with no associated user"


class OrderHistory(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
