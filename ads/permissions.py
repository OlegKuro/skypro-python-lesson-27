from rest_framework.permissions import BasePermission, IsAuthenticated
from typing import List
from ads.models import Advertisement
from users.models import User


class AdOwnerOrHasRoles(BasePermission):
    roles = []

    def __init__(self, *roles: List[str]):
        self.roles = roles

    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, obj: Advertisement):
        user: User = request.user
        return obj.author.pk == user.pk or user.role in self.roles

