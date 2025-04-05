from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from store.models import Product, Variation


def get_cart_id(request: HttpRequest):
    # try:
    #     cart_id = request.session["cart_id"]
    # except KeyError:
    #     if request.user.is_authenticated:
    #         cart, _ = Cart.objects.get_or_create(user=request.user)
    #         cart_id = cart.id
    #     else:
    # cart_id = request.session.session_key
    # if not cart_id:
    #     cart_id = request.session.create()
    return request.session.get("cart_id")


@login_required
def add_cart(request: HttpRequest, product_id):
    """Add product to cart"""
#def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variations = []
    if request.method == "POST":
        for key in request.POST:
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variations.append(variation)
            except Exception as e:
                for arg in e.args:
                    print(f"{arg}")
    stock = product.stock
    check_stock = False
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=get_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    if stock >= cart_item.quantity:
        check_stock = True
    if check_stock:
        return redirect("cart")
    else:
        quantity = cart_item.quantity
        context = {
            "check_stock": check_stock,
            "stock": stock,
            "quantity": quantity,
            "product": Product,
        }
        return render(request, "store/stock_warning.html", context)


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart")


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=get_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart")


@login_required
def get_cart(request: HttpRequest):
    total = 0
    quantity = 0
    cart_items = []
    items_count = 0
    tax = 0
    grand_total = 0
    context = {}
    try:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        items_count = cart_items.count()
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except Exception as e:
        print(f"{e.args}")
    context = {
        "total": total,
        "tax": tax,
        "grand_total": grand_total,
        "cart_items": cart_items,
        "quantity": quantity,
        "items_count": items_count,
    }
    return render(request, "store/cart.html", context)


def place_order(request: HttpRequest):
    return render(request, "store/place-order.html")
