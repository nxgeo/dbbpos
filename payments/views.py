from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from orders.models import OrderItem
from payments.models import Bill


@require_GET
def display_bill(request, bill_id):
    session_key = request.session.session_key

    bill = get_object_or_404(
        Bill.objects.select_related(
            "order", "transaction__payment_method"
        ).prefetch_related(
            Prefetch(
                "order__items", queryset=OrderItem.objects.select_related("product")
            )
        ),
        bill_id=bill_id,
        order__session_key=session_key,
    )
    order = bill.order
    order_items = order.items.all()
    total_amount = sum(order_item.subtotal for order_item in order_items)
    bill_status = bill.get_status_display()
    payment_method = bill.transaction.payment_method

    return render(
        request,
        "payments/bill.html",
        {
            "bill": bill,
            "order": order,
            "order_items": order_items,
            "total_amount": total_amount,
            "bill_status": bill_status,
            "payment_method": payment_method,
        },
    )
