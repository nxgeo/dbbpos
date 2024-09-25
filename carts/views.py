from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from carts.models import Cart, CartItem
from menus.models import Product


class CartView(View):
    http_method_names = ["get", "post", "delete"]

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and "_method" in request.POST:
            request.method = request.POST["_method"].upper()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        session_key = request.session.session_key

        cart, created = Cart.objects.prefetch_related(
            Prefetch("items", queryset=CartItem.objects.select_related("product"))
        ).get_or_create(session_key=session_key)

        if created:
            cart_items = []
            cart_total = 0
        else:
            cart_items = cart.items.all()

            cart_items_to_delete = []
            cart_items_to_update = []

            for cart_item in cart_items:
                current_stock = cart_item.product.stock
                if not cart_item.product.is_active or current_stock == 0:
                    cart_items_to_delete.append(cart_item.pk)
                elif cart_item.quantity > current_stock:
                    cart_item.quantity = current_stock
                    cart_items_to_update.append(cart_item)

            if cart_items_to_delete:
                CartItem.objects.filter(pk__in=cart_items_to_delete).delete()

            if cart_items_to_update:
                CartItem.objects.bulk_update(cart_items_to_update, ["quantity"])

            if cart_items_to_delete or cart_items_to_update:
                cart_items = cart_items.all()

            cart_total = sum(cart_item.subtotal for cart_item in cart_items)

        return render(
            request,
            "carts/cart.html",
            {"cart_id": cart.pk, "cart_items": cart_items, "cart_total": cart_total},
        )

    def post(self, request):
        try:
            product_id = request.POST["product-id"]
        except KeyError:
            raise BadRequest

        product = get_object_or_404(Product, pk=product_id)

        if not product.is_active:
            messages.error(
                request, "An error occurred. Unable to add the product to your cart."
            )
            return redirect("index")

        if product.stock == 0:
            messages.error(request, f"{product.name} is out of stock.")
            return redirect("index")

        session_key = request.session.session_key
        cart = Cart.objects.get_or_create(session_key=session_key)[0]
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": 1}
        )

        if not created:
            new_quantity = cart_item.quantity + 1
            if new_quantity <= product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                messages.error(
                    request,
                    f"Only {product.stock} unit(s) of {product.name} are available, and you already have {cart_item.quantity} in your cart.",
                )
                return redirect("index")

        messages.success(request, f"{product.name} added to your cart.")
        return redirect("index")

    def delete(self, request):
        try:
            cart_item_id = request.POST["cart-item-id"]
        except KeyError:
            raise BadRequest

        session_key = request.session.session_key
        cart_item = get_object_or_404(
            CartItem, cart__session_key=session_key, pk=cart_item_id
        )

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("cart")
