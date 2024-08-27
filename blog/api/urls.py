from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")


urlpatterns = [
    path("", include(router.urls)),
    path("me/", views.UserViewSet.as_view({"get": "retrieve"}), name="me-detail"),
    path(
        "me/change_password/",
        lambda request: redirect(request.get_full_path().replace("me", "users"), permanent=True),
        name="redirect-change-password",
    ),
    path("me/posts/", views.PostList.as_view(), name="me-posts"),
    path("me/comments/", views.CommentList.as_view(), name="me-comments"),
    path("users/<int:user_id>/posts/", views.PostList.as_view(), name="user-posts"),
    path("users/<int:user_id>/comments/", views.CommentList.as_view(), name="user-comments"),
    path("posts/", views.PostList.as_view(), name="posts"),
    path("posts/create/", views.PostCreate.as_view(), name="post-create"),
    path("posts/<int:pk>/", views.PostDetail.as_view(), name="post-detail"),
    path("posts/<int:post_id>/comments/", views.CommentList.as_view(), name="post-comments"),
    path("posts/<int:post_id>/comments/create/", views.CommentCreate.as_view(), name="post-comment-create"),
    path("comments/", views.CommentList.as_view(), name="comment-list"),
    path("comments/<int:pk>", views.CommentDetail.as_view(), name="comment-detail"),
]
