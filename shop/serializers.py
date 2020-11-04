from rest_framework import serializers
from .models import Category, Product, Image, Order, OrderItem
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
        fields = ["id", "name"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product"]

    def get_product(self, obj):
        item = Product.objects.get(id=obj.product.id)
        return ProductSerializer(item).data


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "buyer", "items"]


class CreateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
