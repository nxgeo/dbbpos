from django.urls import path

from menus import views

urlpatterns = [
    path("", views.display_menus, name="index"),
]
