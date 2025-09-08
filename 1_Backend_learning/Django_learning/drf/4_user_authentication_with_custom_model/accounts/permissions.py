from rest_framework.permissions import BasePermission

class isAdmin(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authendicated and request.user.role=="admin"

class isStuff(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role=="stuff"

class isUser(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.role=="user"