from django.db import models

from orders.models import Order


class PaymentMethod(models.Model):
    payment_method_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_method"

    def __str__(self):
        return self.name


class Bill(models.Model):
    class Status(models.IntegerChoices):
        OPEN = 1
        PAID = 2
        VOID = 3

    bill_id = models.AutoField(primary_key=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=Status, default=Status.OPEN)

    class Meta:
        db_table = "bill"

    def __str__(self):
        return f"Bill #{self.bill_id}"


class Transaction(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1
        SUCCESS = 2
        FAILED = 3
        REFUNDED = 4

    transaction_id = models.AutoField(primary_key=True)
    bill = models.OneToOneField(Bill, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount_paid = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=Status, default=Status.PENDING)

    class Meta:
        db_table = "transaction"

    def __str__(self):
        return f"Transaction #{self.transaction_id}"

    @property
    def change_due(self):
        return self.amount_paid - self.bill.total_amount
