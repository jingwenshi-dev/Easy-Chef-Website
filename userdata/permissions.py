from rest_framework.permissions import BasePermission

class RatingOwnershipPermission(BasePermission):
    def has_permission(self, request, view):
        rid = view.kwargs.get('rid')
        user = request.user
