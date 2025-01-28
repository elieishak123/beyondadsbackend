
from rest_framework.permissions import BasePermission, SAFE_METHODS


"""
For this website theres no users, only the admin super user
"""


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin (superuser) to edit or delete, 
    but anyone can view (GET).
    """
    def has_permission(self, request, view):
        # Allow anyone to view (safe methods: GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Allow only superusers to modify content
        return request.user and request.user.is_superuser
