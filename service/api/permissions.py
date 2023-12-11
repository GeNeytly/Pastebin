from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """The user is authenticated and he is author of obj"""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author


class IsAuthorOrListObjects(permissions.BasePermission):
    """The user is authenticated and either he is
    the author of the post or a read request."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.post.author or request.method == 'GET'
