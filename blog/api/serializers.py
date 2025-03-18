from django.contrib.auth.password_validation import validate_password
from drf_queryfields import QueryFieldsMixin  # type: ignore[import-untyped]
from rest_framework import serializers

from . import models


class CommentSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer[models.Comment]):  # type: ignore[misc]
    class Meta:
        model = models.Comment
        fields = ("id", "post", "content", "created_by", "created_at", "changed_by", "changed_at")
        read_only_fields = ("post", "created_by", "created_at", "changed_by", "changed_at")


class PostSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer[models.Post]):  # type: ignore[misc]
    # post_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Post
        fields = ("id", "title", "content", "created_by", "created_at", "changed_by", "changed_at", "post_comments")
        read_only_fields = ("created_by", "created_at", "changed_by", "changed_at", "post_comments")


class UserSerializer(QueryFieldsMixin, serializers.HyperlinkedModelSerializer[models.User]):  # type: ignore[misc]
    class Meta:
        model = models.User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "last_login",
            "date_joined",
            "is_staff",
            "created_posts",
            "created_comments",
        )


class ChangePasswordSerializer(QueryFieldsMixin, serializers.Serializer[models.User]):  # type: ignore[misc]
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value: str) -> str:
        validate_password(value)
        return value
