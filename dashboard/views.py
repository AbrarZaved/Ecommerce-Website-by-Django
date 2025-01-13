from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from product.models import Product

# Create your views here.


def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        products = Product.objects.filter(title__icontains=title).order_by("-rating")
    else:
        products = Product.objects.all().order_by("-rating")

    # Paginate the products
    paginator = Paginator(products, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/index.html",
        {
            "products": page_obj,
            "title": title if request.method == "POST" else "",
            "page_obj": page_obj,
        },
    )


def product_by_categories(request, sub_category=None):
    if not sub_category:
        return redirect("index")
    products = Product.objects.filter(sub_category__icontains=sub_category).order_by(
        "-rating"
    )
    paginator = Paginator(products, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "dashboard/index.html",
        {"products": page_obj, "page_obj": page_obj},
    )
