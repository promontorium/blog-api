from django.contrib.auth.models import User
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import models, permissions, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("id", "username", "first_name", "last_name", "email", "is_staff", "last_login", "date_joined")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering_fields = ("id", "username", "first_name", "last_name", "email", "last_login", "date_joined")

    def retrieve(self, request, pk=None):
        if pk is not None:
            return super().retrieve(request, pk)
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["patch"],
        permission_classes=[IsAuthenticated],
        name="Change Password",
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


class PostList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("title", "content")
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        if "/me/" in self.request.path:  # TODO
            return models.Post.objects.filter(created_by=self.request.user)

        user_id = self.kwargs.get("user_id")
        if user_id is None:
            return models.Post.objects.all()

        if not User.objects.filter(id=user_id).exists():
            raise NotFound(f"No {User._meta.object_name} matches the given query.")

        return models.Post.objects.filter(created_by=user_id)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)


class PostCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PostSerializer
    queryset = models.Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentList(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = "__all__"
    search_fields = ("content",)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        if post_id is not None:
            if not models.Post.objects.filter(id=post_id).exists():
                raise NotFound(f"No {models.Post._meta.object_name} matches the given query.")
            return models.Comment.objects.filter(post_id=post_id)

        if "/me/" in self.request.path:  # TODO
            return models.Comment.objects.filter(created_by=self.request.user)

        user_id = self.kwargs.get("user_id")
        if user_id is None:
            return models.Comment.objects.all()

        if not User.objects.filter(id=user_id).exists():
            raise NotFound(f"No {User._meta.object_name} matches the given query.")

        return models.Comment.objects.filter(created_by=user_id)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsReadOnly | permissions.IsOwner | IsAdminUser,)
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def perform_update(self, serializer):
        serializer.validated_data["changed_by"] = self.request.user
        serializer.validated_data["changed_at"] = timezone.now()
        return super().perform_update(serializer)


class CommentCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        if not models.Post.objects.filter(id=post_id).exists():
            raise ValidationError("Invalid post_id.")
        serializer.save(post_id=post_id, created_by=self.request.user)
