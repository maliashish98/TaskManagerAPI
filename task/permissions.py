from rest_framework.permissions import BasePermission

class IsSelforAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff():
            return True
        return obj == request.user
    
class IsTaskOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff