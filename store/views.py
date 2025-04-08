from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from cart.models import Cart, CartItem
from cart.views import get_cart_id
from category.models import Category
from store.forms import ProductForm
from store.models import Product


def home(request: HttpRequest):
    # 10 random products
    products = Product.objects.filter(is_available=True).order_by("?")[:10]
    context = {"products": products}

    return render(request, "home.html", context=context)


def store(request, category_slug=None):
    products = ""
    category = category_slug
    if category:
        category = get_object_or_404(Category, slug=category_slug)
        products = (
            Product.objects.all()
            .filter(category=category, is_available=True)
            .order_by("-id")
        )
        paginator = Paginator(products, 1)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
    else:
        products = Product.objects.all().filter(is_available=True).order_by("-id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
    context = {
        "products": paged_products,
        "total": products.count(),
        "category": category,
    }
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    is_cart_item = False
    p = get_object_or_404(Product, slug=product_slug)
    cart_id = get_cart_id(request)
    cart = Cart.objects.filter(cart_id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart[:1])
    category_slug2 = category_slug
    for item in cart_items:
        if item.product.id == p.id:
            is_cart_item = True
    context = {
        "p": p,
        "category_slug": category_slug2,
        "is_cart_item": is_cart_item,
    }
    return render(request, "store/product_detail.html", context)


def search(request):
    kw = ""
    if "keyword" in request.GET:
        kw = request.GET["keyword"]
    # if kw != '':
    # if kw:
    products = Product.objects.all().filter(
        Q(product_name__icontains=kw) | Q(description__icontains=kw)
    )
    # paginator = Paginator(products, 10)
    # page = request.GET.get('page')
    # paged_products = paginator.get_page(page)
    context = {
        "products": products,
        "total": products.count(),
        "keyword": kw,
    }
    return render(request, "store/store.html", context)
    # else:
    #     return redirect('store')
    # else:
    #     return redirect('store')


def product_update(request: HttpRequest, id):
    product = get_object_or_404(Product, id=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message="Product updated successfully.", extra_tags="success")
            return redirect("product_list")
        else:
            messages.error(
                request=request, message="Error updating product.", extra_tags="danger")
            return render(
                request=request,
                template_name="store/product_update.html",
                context={"form": form, "product": product},
            )
    else:
        form = ProductForm(instance=product)
        return render(
            request=request,
            template_name="store/product_update.html",
            context={"form": form, "product": product},
        )


def product_delete(request: HttpRequest, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    messages.success(
        request=request, message="Product deleted successfully.", extra_tags="success")
    return redirect("product_list")


def product_create(request: HttpRequest):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message="Product created successfully.", extra_tags="success")
            return redirect("product_list")
        else:
            messages.error(
                request=request, message="Error creating product.", extra_tags="danger")
            return render(
                request=request,
                template_name="store/product_create.html",
                context={"form": form},
            )
    else:
        form = ProductForm()
        return render(
            request=request,
            template_name="store/product_create.html",
            context={"form": form},
        )


def product_list(request: HttpRequest):
    products = Product.objects.all()
    paginator = Paginator(products, 10)
    page = request.GET.get("page")
    paged_products = paginator.get_page(page)
    context = {
        "products": paged_products,
        "total": products.count(),
    }
    return render(request, "store/product_list.html", context)
