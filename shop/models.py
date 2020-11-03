from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    inventory = models.PositiveSmallIntegerField()
    date_added = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    main_image = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.category.name} - {self.price} - {self.inventory}"


class Image(models.Model):
    img = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.product.name


class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Address(models.Model):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name="locations")
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return f"{self.user.username} - {self.country.name} - {self.city}"


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    datetime = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, related_name="deliveries", null=True, blank=True)

    def __str__(self):
        return f"{self.buyer.username} on {self.datetime} total: {self.total}"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="items")
    quantity = models.PositiveSmallIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.order.buyer.username} item: {self.product.name} qty: {self.quantity}"
