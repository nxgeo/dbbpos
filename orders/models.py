from django.db import models

from menus.models import Product


class Order(models.Model):
    class Status(models.IntegerChoices):
        AWAITING_PAYMENT = 1
        PROCESSING = 2
        COMPLETED = 3
        CANCELED = 4

    order_id = models.AutoField(primary_key=True)
    session_key = models.CharField(max_length=40)
    customer_name = models.CharField(max_length=70)
    customer_email = models.EmailField()
    customer_phone_number = models.CharField(max_length=15)
    table_number = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(
        choices=Status, default=Status.AWAITING_PAYMENT
    )

    class Meta:
        db_table = "order"

    def __str__(self):
        return f"Order #{self.order_id}"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "order_item"

    @property
    def subtotal(self):
        return self.price * self.quantity
