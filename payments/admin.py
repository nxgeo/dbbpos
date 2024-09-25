from django.contrib import admin

from payments.models import Bill, PaymentMethod, Transaction

admin.site.register(PaymentMethod)
admin.site.register(Bill)
admin.site.register(Transaction)
