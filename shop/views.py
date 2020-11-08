from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from django.db.models import Sum, F, FloatField
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Category, Product, Image, Order, OrderItem, Address, Country
from .serializers import (
    ProductsListSerializer, RegisterSerializer, CartSerializer,
    CreateOrderItemSerializer, CheckoutSerializer, OrderItemSerializer, UserProfileSerializer,
    UpdateUserSerializer, CountrySerializer, CreateAddressSerializer
)


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserCart(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)
        return cart


class AddItem(APIView):
    serializer_class = CreateOrderItemSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            valid_data = serializer.data
            cart, _ = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)

            order_item, created = OrderItem.objects.get_or_create(
                product_id=valid_data["product"],
                order=cart
            )

            if created:
                order_item.quantity = valid_data['quantity']
            else:
                order_item.quantity += valid_data['quantity']

            order_item.save()

            json_response = OrderItemSerializer(order_item).data
            return Response(json_response, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteOrderItem(DestroyAPIView):
    queryset = OrderItem.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "order_item_id"


class Checkout(APIView):
    serializer_class = CheckoutSerializer

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            valid_data = serializer.data
            cart = Order.objects.filter(buyer=self.request.user, is_paid=False).first()
            if cart:
                address = Address.objects.get(id=valid_data["address"])
                if cart.items.exists():
                    cart.total = \
                        cart.items.aggregate(total=Sum(F("quantity") * F("product__price"), output_field=FloatField()))[
                            "total"]
                    cart.address = address
                    cart.is_paid = True
                    cart.save()
                    return Response({"total": cart.total}, status=HTTP_200_OK)
            return Response({"msg": "cart is empty"}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserProfile(RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UpdateUserInfo(RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class CountryList(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CreateAddress(CreateAPIView):
    serializer_class = CreateAddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class UpdateDeleteAddress(APIView):
#     serializer_class = CreateAddressSerializer
#
#     def put(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.serializer_class(data=data)
#         if serializer.is_valid():
#             valid_data = serializer.data
#             address = Address.objects.get(id=self.request.data["id"])
#             address.active = False
#             address.save()
#             new_address =