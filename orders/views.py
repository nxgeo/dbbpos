from django.contrib import messages
from django.core.exceptions import BadRequest
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from carts.models import Cart, CartItem
from orders.models import Order, OrderItem
from payments.models import Bill, PaymentMethod, Transaction


def get_cart_and_items(cart_id, session_key):
    cart = get_object_or_404(
        Cart.objects.prefetch_related(
            Prefetch("items", queryset=CartItem.objects.select_related("product"))
        ),
        cart_id=cart_id,
        session_key=session_key,
    )
    cart_items = cart.items.all()
    return cart, cart_items


def validate_cart_items(cart_items):
    if not cart_items.exists():
        return "Your cart is empty."

    for cart_item in cart_items:
        current_stock = cart_item.product.stock
        if not cart_item.product.is_active:
            return f"{cart_item.product.name} is currently unavailable."
        elif current_stock == 0:
            return f"{cart_item.product.name} is out of stock."
        elif cart_item.quantity > current_stock:
            return f"Only {current_stock} unit(s) of {cart_item.product.name} in stock."

    return None


@require_GET
def display_checkout(request):
    try:
        cart_id = request.GET["cart-id"]
    except KeyError:
        raise BadRequest

    session_key = request.session.session_key

    cart, cart_items = get_cart_and_items(cart_id, session_key)

    error_message = validate_cart_items(cart_items)
    if error_message:
        messages.error(request, error_message)
        return redirect("cart")

    cart_total = sum(cart_item.subtotal for cart_item in cart_items)

    payment_methods = PaymentMethod.objects.filter(is_active=True)

    return render(
        request,
        "orders/checkout.html",
        {
            "cart_id": cart_id,
            "cart_items": cart_items,
            "cart_total": cart_total,
            "payment_methods": payment_methods,
        },
    )


@require_POST
@transaction.atomic
def place_order(request):
    try:
        cart_id = request.POST["cart-id"]
        payment_method = request.POST["payment-method"]
        customer_name = request.POST["customer-name"]
        customer_email = request.POST["customer-email"]
        customer_phone_number = request.POST["customer-phone-number"]
        table_number = request.POST["table-number"]
    except KeyError:
        raise BadRequest

    session_key = request.session.session_key

    cart, cart_items = get_cart_and_items(cart_id, session_key)

    error_message = validate_cart_items(cart_items)
    if error_message:
        messages.error(request, error_message)
        return redirect("cart")

    order = Order.objects.create(
        session_key=session_key,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone_number=customer_phone_number,
        table_number=table_number,
    )

    order_items = OrderItem.objects.bulk_create(
        [
            OrderItem(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
            )
            for cart_item in cart_items
        ]
    )

    cart_items.delete()

    for order_item in order_items:
        order_item.product.stock -= order_item.quantity
        order_item.product.save()

    total_amount = sum(order_item.subtotal for order_item in order_items)

    bill = Bill.objects.create(order=order, total_amount=total_amount)

    Transaction.objects.create(bill=bill, payment_method_id=payment_method)

    return redirect("bill", bill_id=bill.pk)
