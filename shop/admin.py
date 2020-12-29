from django.contrib import admin
from .models import Category, Product, Image, Country, Address, Order, OrderItem


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "inventory", "date_added", "category"]
    search_fields = ["name", "category__name"]
    list_filter = ["category"]
    list_editable = ["price"]


admin.site.register(Product, ProductAdmin)

admin.site.register(Image)
admin.site.register(Country)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
