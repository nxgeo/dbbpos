from django.urls import path

from payments import views

urlpatterns = [
    path("bill/<int:bill_id>/", views.display_bill, name="bill"),
]
