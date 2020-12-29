from rest_framework.permissions import BasePermission


class IsCartOwner(BasePermission):
    message = "You must be the cart owner"

    def has_object_permission(self, request, view, obj):
        return obj.order.buyer == request.user
