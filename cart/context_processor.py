from cart.models import Cart


def cart_count(request):
    total_item = 0
    if request.user.is_authenticated:
        try:
            total_item = Cart.objects.filter(user=request.user).count()
        except Exception as e:
            pass

    return {"total_item": total_item}
