import re

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            if re.search(r'/edit.?$', request.META.get('HTTP_REFERER')):
                return obj.author == request.user

            return True

        return obj.author == request.user
