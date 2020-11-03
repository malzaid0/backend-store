from django.contrib import admin
from .models import Category, Product, Image, Country, Address, Order, OrderItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Country)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
