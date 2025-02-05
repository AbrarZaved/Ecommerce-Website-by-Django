from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import F
from authentication.models import Customer
from cart.models import OrderHistory
from product.models import Product, product_review

# Create your views here.


def product_details(request, slug):
    product = Product.objects.get(slug=slug)
    related_products = (
        Product.objects.filter(sub_category=product.sub_category)
        .exclude(slug=slug)
        .order_by("-rating")[:10]
    )
    sub_category = product.sub_category
    product_review_set = product_review.objects.filter(product=product).order_by(
        "-created_at"
    )
    return render(
        request,
        "product/product_details.html",
        {
            "product": product,
            "related_products": related_products,
            "sub_category": sub_category,
            "product_review_set": product_review_set,
        },
    )


def submit_review(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        rating = request.POST.get("rating")
        review = request.POST.get("review")

        # Get the product
        product = OrderHistory.objects.get(id=product_id).product

        # Create and save the review
        product_review.objects.create(
            product=product,
            user=request.user,  # Assuming user is a customer
            rating=rating,
            review=review,
        )
        
        request.user.total_reviews = F("total_reviews") + 1
        request.user.save()
        OrderHistory.objects.filter(id=product_id).update(reviewed=True)
        # Redirect back to the product details page
        messages.success(request, "Review submitted successfully")
        return redirect("product_details", slug=product.slug)

    return redirect("profile")  # Handle any other cases
