from django.urls import path

from orders import views

urlpatterns = [
    path("checkout/", views.display_checkout, name="checkout"),
    path("order/", views.place_order, name="order"),
]
