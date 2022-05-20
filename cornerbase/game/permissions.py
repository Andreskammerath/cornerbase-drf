from rest_framework import permissions

class IscreatorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
    # Read-only permissions are allowed for any request
    # Write permissions are only allowed to the author of a post
        return request.method in permissions.SAFE_METHODS or obj.author == request.user