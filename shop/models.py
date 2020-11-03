from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    inventory = models.PositiveSmallIntegerField()
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.category.name} - {self.price} - {self.inventory}"


class Image(models.Model):
    img = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
