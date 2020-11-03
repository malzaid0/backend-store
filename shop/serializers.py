from rest_framework import serializers
from .models import Category, Product, Image
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

