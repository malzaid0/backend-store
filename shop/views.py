from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .models import Category, Product, Image, Order, OrderItem
from .serializers import ProductsListSerializer, RegisterSerializer, CartSerializer, CreateOrderItemSerializer


class ProductsList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsListSerializer


class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserCart(RetrieveAPIView):
    queryset = Order.objects.filter(is_paid=False)
    lookup_field = "buyer_id"
    lookup_url_kwarg = "user_id"
    serializer_class = CartSerializer


class AddItem(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = CreateOrderItemSerializer
    lookup_field = "buyer_id"
    lookup_url_kwarg = "user_id"

    def perform_create(self, serializer):
        print("kwargs", self.kwargs["user_id"])
        user = User.objects.get(id=int(self.kwargs["user_id"]))
        print("user", user)
        cart = user.orders.filter(is_paid=False).first()
        print("cart", cart)
        # cart = self.request.user.orders.filter(is_paid=False)
        if cart:
            exists = False
            # items = OrderItem.objects.filter(order=cart)
            print("cart items", cart.items.all())
            for item in cart.items.all():
                print(item.product.id)
                if item.product.id == int(self.request.data["product"]):
                    exists = True
                    print("Exists", item)
                    item.quantity += int(self.request.data["quantity"])
                    item.save()
            if not exists:
                new_item = {
                    "product": Product.objects.get(id=int(self.request.data["product"])),
                    "quantity": self.request.data["quantity"],
                    "order": cart
                }
                serializer.save(**new_item)
        else:
            # new_order = Order.objects.create(buyer=self.request.user)
            new_order = Order.objects.create(buyer=user)
            print("new order", new_order)
            new_item = {
                "product": Product.objects.get(id=self.request.data["product"]),
                "quantity": self.request.data["quantity"],
                "order": new_order
            }
            serializer.save(**new_item)
