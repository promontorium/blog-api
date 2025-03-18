from typing import Sequence

from django.db.models.query import QuerySet
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend  # type: ignore[import-untyped]
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

from . import models, permissions, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet[models.User]):
    ME_PK = "me"
    queryset = models.User.objects
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("id", "username", "first_name", "last_name", "email", "last_login", "date_joined")

    @action(detail=False, methods=["get"], permission_classes=(IsAuthenticated,), url_path=ME_PK)
    def me(self, request: Request) -> Response:
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=(IsAuthenticated,),
        serializer_class=serializers.ChangePasswordSerializer,
    )
    def change_password(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not self.request.user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ReadOnlyModelViewSet[models.Post], mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("title", "content")
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)

    def get_queryset(self) -> QuerySet[models.Post]:
        result = models.Post.objects.all()
        user_id = self.kwargs.get("user_pk")
        if user_id is not None:
            user_id = self.request.user.id if user_id == UserViewSet.ME_PK else user_id  # type: ignore[union-attr]
            result = result.filter(created_by=user_id)
        return result  # type: ignore[no-any-return]

    def perform_update(self, serializer: BaseSerializer[models.Post]) -> None:
        serializer.save(changed_by=self.request.user, changed_at=timezone.now())


class PostCreateView(CreateAPIView[models.Post]):
    serializer_class = serializers.PostSerializer
    viewsets = models.Post.objects
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer: BaseSerializer[models.Post]) -> None:
        serializer.save(created_by=self.request.user)


class CommentViewSet(viewsets.ModelViewSet[models.Comment]):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("content",)
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)

    def get_permissions(self) -> Sequence[BasePermission]:
        if self.action == "create":
            return (IsAuthenticated(),)
        return super().get_permissions()  # type: ignore[return-value]

    def get_queryset(self) -> QuerySet[models.Comment]:
        result = models.Comment.objects.all()
        post_id = self.kwargs.get("post_pk")
        if post_id is not None:
            result = result.filter(post_id=post_id)
        user_id = self.kwargs.get("user_pk")
        if user_id is not None:
            user_id = self.request.user.id if user_id == UserViewSet.ME_PK else user_id  # type: ignore[union-attr]
            result = result.filter(created_by=user_id)
        return result  # type: ignore[no-any-return]

    def perform_create(self, serializer: BaseSerializer[models.Comment]) -> None:
        post_id = self.kwargs.get("post_pk")
        if not models.Post.objects.filter(id=post_id).exists():
            raise ValidationError("Invalid post_pk.")
        serializer.save(post_id=post_id, created_by=self.request.user)

    def perform_update(self, serializer: BaseSerializer[models.Comment]) -> None:
        serializer.save(changed_by=self.request.user, changed_at=timezone.now())
