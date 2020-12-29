from rest_framework import serializers
from .models import Category, Product, Image, Order, OrderItem, Country, Address
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(allow_null=False, allow_blank=False)
    last_name = serializers.CharField(allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', "email"]

    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return validated_data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "img"]


class ProductsListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "inventory", "date_added", "description", "main_image", "category", "images"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "main_image", "inventory"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product"]


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "buyer", "items"]


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class AddressSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Address
        fields = ["id", "country", "city", "street", "phone"]


class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["address"]


class PreviousOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ["id", "datetime", "total", "is_paid", "address", "items"]


class UserProfileSerializer(serializers.ModelSerializer):
    previous_orders = serializers.SerializerMethodField()
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "previous_orders", "addresses"]

    def get_previous_orders(self, obj):
        orders = obj.orders.filter(is_paid=True)
        return PreviousOrderSerializer(orders, many=True).data

    def get_addresses(self, obj):
        active_addresses = obj.addresses.filter(active=True)
        return AddressSerializer(active_addresses, many=True).data


class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_null=False, allow_blank=False)
    last_name = serializers.CharField(allow_null=False, allow_blank=False)
    email = serializers.EmailField(allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["country", "city", "street", "phone"]

    def to_representation(self, instance):
        return AddressSerializer(instance).data
