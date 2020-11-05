from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import Category, Product, Image, Order, OrderItem, Address
from .serializers import ProductsListSerializer, RegisterSerializer, CartSerializer, CreateOrderItemSerializer, CheckoutSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserCart(RetrieveAPIView):
    queryset = Order.objects.all()
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
            cart, created = Order.objects.get_or_create(buyer=self.request.user, is_paid=False)
            if created:
                new_item = {
                    "product": Product.objects.get(id=valid_data["product"]),
                    "quantity": valid_data["quantity"],
                    "order": cart
                }
                new_order_item = OrderItem.objects.create(**new_item)
                return Response({
                    "product": new_order_item.product.name,
                    "quantity": valid_data["quantity"],
                    "order": cart.buyer.username
                }, status=HTTP_200_OK)

            else:
                for item in cart.items.all():
                    if item.product.id == int(valid_data["product"]):
                        item.quantity += int(valid_data["quantity"])
                        item.save()
                        return Response({
                            "product": {
                                "id": item.product.id,
                                "name": item.product.name,
                                "price": item.product.price,
                                "main_image": item.product.main_image
                            },
                            "quantity": item.quantity,
                            "id": item.id,
                        }, status=HTTP_200_OK)

                new_item = {
                    "product": Product.objects.get(id=int(valid_data["product"])),
                    "quantity": valid_data["quantity"],
                    "order": cart
                }
                new_order_item = OrderItem.objects.create(**new_item)
                return Response({
                    "product": new_order_item.product.name,
                    "quantity": valid_data["quantity"],
                    "order": cart.buyer.username
                }, status=HTTP_200_OK)

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
            cart = Order.objects.get(buyer=self.request.user, is_paid=False)
            address = Address.objects.get(id=valid_data["address"])
            if cart.items.all().exists():
                for item in cart.items.all():
                    cart.total += item.product.price * item.quantity
                cart.address = address
                cart.is_paid = True
                cart.save()
                return Response({"total": cart.total}, status=HTTP_200_OK)
            return Response("cart is empty", status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
