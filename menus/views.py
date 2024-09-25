from django.db.models import Prefetch
from django.shortcuts import render
from django.views.decorators.http import require_GET

from menus.models import Category, Product


@require_GET
def display_menus(request):
    categories = Category.objects.prefetch_related(
        Prefetch(
            "products",
            queryset=Product.objects.filter(is_active=True),
            to_attr="active_products",
        )
    )
    return render(request, "menus/index.html", {"categories": categories})
