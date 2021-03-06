"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("products/", views.ProductsList.as_view(), name="products"),
    path("countries/", views.CountryList.as_view(), name="countries"),

    path("addresses/create/", views.CreateAddress.as_view(), name="add-address"),
    path("addresses/update/", views.UpdateDeleteAddress.as_view(), name="update-address"),

    path("order-items/<int:order_item_id>/", views.DeleteOrderItem.as_view(), name="del-order-item"),

    path('cart/', views.UserCart.as_view(), name="cart"),
    path('cart/add/', views.AddItem.as_view(), name="add-item"),
    path('checkout/', views.Checkout.as_view(), name="checkout"),

    path('profile/', views.UserProfile.as_view(), name="profile"),
    path('profile/update/', views.UpdateUserInfo.as_view(), name="update-user"),

    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token-refresh"),
    path('register/', views.Register.as_view(), name="register"),
]
