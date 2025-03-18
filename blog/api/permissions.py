from typing import Any

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool:
        return obj.created_by == request.user  # type: ignore[no-any-return]


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return request.method in permissions.SAFE_METHODS
