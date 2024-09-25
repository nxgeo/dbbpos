from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("menus.urls")),
    path("", include("carts.urls")),
    path("", include("orders.urls")),
    path("", include("payments.urls")),
]
