from django.urls import path

from . import views

urlpatterns = [
    path("change-password/", views.ChangePassword.as_view(), name="change-password"),
    path("users/", views.UserList.as_view(), name="users"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("users/<int:user_id>/posts/", views.UserPostList.as_view(), name="user-posts"),
    path("users/<int:user_id>/comments/", views.UserCommentList.as_view(), name="user-comments"),
    path("me/", views.MeUserDetail.as_view(), name="me"),
    path("me/posts/", views.MePostList.as_view(), name="me-posts"),
    path("me/comments/", views.MeCommentList.as_view(), name="me-comments"),
    path("posts/", views.PostList.as_view(), name="posts"),
    path("posts/<int:pk>/", views.PostDetail.as_view(), name="post-detail"),
    path("posts/<int:post_id>/comments/", views.CommentList.as_view(), name="post-comments"),
    path("posts/<int:post_id>/comments/<int:pk>/", views.CommentDetail.as_view(), name="post-comment-detail"),
]
