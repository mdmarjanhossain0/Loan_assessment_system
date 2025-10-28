from rest_framework.permissions import BasePermission

from account.models import (
    Account,
)

class OrPermission(BasePermission):

    def __init__(self, *permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return any(permission().has_permission(request, view) for permission in self.permissions)

    def has_object_permission(self, request, view, obj):
        return any(permission().has_object_permission(request, view, obj) for permission in self.permissions)

class LoanPostermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        is_authenticated = request.user and request.user.is_authenticated
        if is_authenticated:
            if request.user.role == Account.ADMIN:
                return True
        return False