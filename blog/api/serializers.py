from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.HyperlinkedRelatedField(read_only=True, view_name="post-detail")

    class Meta:
        model = Comment
        fields = ("id", "post", "content", "created_by", "created_at", "changed_by", "changed_at")
        read_only_fields = ("created_by", "created_at", "changed_by", "changed_at")


class PostSerializer(serializers.ModelSerializer):
    post_comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ("id", "title", "content", "created_by", "created_at", "changed_by", "changed_at", "post_comments")
        read_only_fields = ("created_by", "created_at", "changed_by", "changed_at")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
