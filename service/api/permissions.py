from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """The user is authenticated and he is author of obj."""

    def has_permission(self, request, view):
        """User is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """The request user and the obj.author are the same person."""
        return request.user == obj.author


class IsAuthorOrReadOnly(permissions.BasePermission):
    """The user is authenticated and either he is
    the author of the post or a read request."""

    def has_permission(self, request, view):
        """User is authenticated."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """The request user and the obj.author are the same
        person or GET request."""
        return request.user == obj.post.author or request.method == 'GET'
