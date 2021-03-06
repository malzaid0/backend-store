from django.db.models import Sum, F, FloatField
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .models import Product, Order, OrderItem, Address, Country
from .permissions import IsCartOwner
from .serializers import (
    ProductsListSerializer, RegisterSerializer, CartSerializer,
    CreateOrderItemSerializer, OrderItemSerializer, UserProfileSerializer,
    UpdateUserSerializer, CountrySerializer, CreateAddressSerializer
)


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserCart(RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)
        cart.clean()
        return cart


class AddItem(APIView):
    serializer_class = CreateOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)
        return cart

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            valid_data = serializer.data
            cart = self.get_object()

            order_item, created = OrderItem.objects.get_or_create(
                product_id=valid_data["product"],
                order=cart
            )
            order_item.update_quantity(created, valid_data['quantity'], True)

            json_response = OrderItemSerializer(order_item).data
            return Response(json_response, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            valid_data = serializer.data
            cart = self.get_object()

            order_item, created = OrderItem.objects.get_or_create(
                product_id=valid_data["product"],
                order=cart
            )
            order_item.update_quantity(created, valid_data['quantity'], False)

            json_response = OrderItemSerializer(order_item).data
            return Response(json_response, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DeleteOrderItem(DestroyAPIView):
    queryset = OrderItem.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "order_item_id"
    permission_classes = [IsAuthenticated, IsCartOwner]


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            address = Address.objects.get(id=request.data['address'])
        except:
            return Response({"msg": "Address does not exist"}, status=HTTP_400_BAD_REQUEST)
        else:
            cart, _ = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)
            if cart.items.exists():
                if cart.items_in_stock():
                    for item in cart.items.all():
                        item.product.inventory -= item.quantity
                        item.product.save()
                    cart.total = cart.items.aggregate(
                        total=Sum(F("quantity") * F("product__price"), output_field=FloatField())
                    )["total"]
                    cart.address = address
                    cart.is_paid = True
                    cart.save()
                    return Response({"total": cart.total}, status=HTTP_200_OK)
                else:
                    return Response({"msg": "Some items in your cart have exceeded the available inventory"},
                                    status=HTTP_400_BAD_REQUEST)
            return Response({"msg": "cart is empty"}, status=HTTP_400_BAD_REQUEST)


class UserProfile(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdateUserInfo(RetrieveUpdateAPIView):
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CountryList(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CreateAddress(CreateAPIView):
    serializer_class = CreateAddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateDeleteAddress(APIView):
    serializer_class = CreateAddressSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            address = Address.objects.get(id=self.request.data["id"])
            address.active = False
            address.save()
            new_address = serializer.save(user=self.request.user)
            json_response = CreateAddressSerializer(new_address).data
            return Response(json_response, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    # This's actually delete
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            address = Address.objects.get(id=self.request.data["id"])
            address.active = False
            address.save()
            return Response({"msg": "address has been deleted"}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
