from django.db import models

from menus.models import Product


class Cart(models.Model):
    cart_id = models.SmallAutoField(primary_key=True)
    session_key = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "cart"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        db_table = "cart_item"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_cart_product"
            )
        ]

    @property
    def subtotal(self):
        return self.product.price * self.quantity
