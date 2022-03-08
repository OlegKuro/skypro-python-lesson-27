from rest_framework.permissions import BasePermission, IsAuthenticated
from selections.models import Selection


class IsSelectionAuthor(BasePermission):
    message = 'You are not allowed to mutate this object'

    def has_object_permission(self, request, view, obj: Selection):
        return obj.author.pk == request.user.pk

    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view)

