from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Klient'

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Sprzedawca'