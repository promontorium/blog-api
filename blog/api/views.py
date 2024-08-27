from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import models, permissions, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    ME_PK = "me"
    queryset = User.objects
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("id", "username", "first_name", "last_name", "email", "last_login", "date_joined")

    @action(detail=False, methods=["get"], permission_classes=(IsAuthenticated,), url_path=ME_PK)
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=(IsAuthenticated,),
        serializer_class=serializers.ChangePasswordSerializer,
    )
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not self.request.user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("title", "content")
    serializer_class = serializers.PostSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return (permissions.IsOwnerOrAdmin(),)
        return (IsAuthenticatedOrReadOnly(),)

    def get_queryset(self):
        result = models.Post.objects
        user_id = self.kwargs.get("user_pk")
        if user_id is not None:
            user_id = self.request.user.id if user_id == UserViewSet.ME_PK else user_id
            result = result.filter(created_by=user_id)
        return result

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("content",)
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsReadOnly | permissions.IsOwnerOrAdmin,)

    def get_permissions(self):
        if self.action == "create":
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        result = models.Comment.objects
        post_id = self.kwargs.get("post_pk")
        if post_id is not None:
            result = result.filter(post_id=post_id)
        user_id = self.kwargs.get("user_pk")
        if user_id is not None:
            user_id = self.request.user.id if user_id == UserViewSet.ME_PK else user_id
            result = result.filter(created_by=user_id)
        return result

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_pk")
        if not models.Post.objects.filter(id=post_id).exists():
            raise ValidationError("Invalid post_pk.")
        serializer.save(post_id=post_id, created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)
