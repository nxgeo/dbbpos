from django.db import models


class Category(models.Model):
    category_id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


def get_sentinel_category():
    return Category.objects.get_or_create(name="Unknown")[0]


class Product(models.Model):
    product_id = models.SmallAutoField(primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET(get_sentinel_category), related_name="products"
    )
    name = models.CharField(max_length=40, unique=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name
