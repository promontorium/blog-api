from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from . import models, permissions, serializers


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("id", "username", "first_name", "last_name", "email", "last_login", "date_joined")


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserPostList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("title", "content")
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return models.Post.objects.filter(created_by=user_id)


class UserCommentList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("content",)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return models.Comment.objects.filter(created_by=user_id)


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("title", "content")
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)


class CommentList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("content",)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        result = models.Post.objects.filter(id=post_id)
        if not result.exists():
            raise NotFound(f"No {models.Post._meta.object_name} matches the given query.")
        return result

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(post_id=post_id, created_by=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        result = models.Post.objects.filter(id=post_id)
        if not result.exists():
            raise NotFound(f"No {models.Post._meta.object_name} matches the given query.")
        return result

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)


class ChangePassword(views.APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if not self.request.user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        self.request.user.set_password(serializer.data.get("new_password"))
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
