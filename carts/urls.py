from django.urls import path

from carts import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
]
