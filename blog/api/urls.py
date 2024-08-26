from django.urls import path

from .views import (
    ChangePassword,
    CommentDetail,
    CommentList,
    PostDetail,
    PostList,
    UserCommentList,
    UserDetail,
    UserList,
    UserPostList,
)

urlpatterns = [
    path("change-password", ChangePassword.as_view(), name="change-password"),
    path("users/", UserList.as_view(), name="users"),
    path("users/<int:pk>", UserDetail.as_view(), name="user-detail"),
    path("users/<int:user_id>/posts", UserPostList.as_view(), name="user-posts"),
    path("users/<int:user_id>/comments", UserCommentList.as_view(), name="user-comments"),
    path("posts/", PostList.as_view(), name="posts"),
    path("posts/<int:pk>", PostDetail.as_view(), name="post-detail"),
    path("posts/<int:post_id>/comments/", CommentList.as_view(), name="post-comments"),
    path("posts/<int:post_id>/comments/<int:pk>", CommentDetail.as_view(), name="post-comment-detail"),
]
