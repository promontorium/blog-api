from django.urls import path

from .views import (
    ChangePassword,
    CommentDetail,
    CommentList,
    PostDetail,
    PostList,
    UserDetail,
    UserList,
)

urlpatterns = [
    path("change-password", ChangePassword.as_view(), name="change-password"),
    path("users/", UserList.as_view(), name="users"),
    path("users/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("posts/", PostList.as_view(), name="posts"),
    path("posts/<int:pk>", PostDetail.as_view(), name="post-detail"),
    path("posts/<int:post_id>/comments/", CommentList.as_view(), name="post-comments"),
    path("posts/<int:post_id>/comments/<int:pk>", CommentDetail.as_view(), name="post-comment-detail"),
]
