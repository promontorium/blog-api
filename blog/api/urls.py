from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")
router.register(r"me/posts", views.PostViewSet, basename="me-post")
router.register(r"me/comments", views.CommentViewSet, basename="me-comment")

user_nested_router = NestedDefaultRouter(router, r"users", lookup="user")
user_nested_router.register(r"posts", views.PostViewSet, basename="user-post")
user_nested_router.register(r"comments", views.CommentViewSet, basename="user-comment")

post_nested_router = NestedDefaultRouter(router, r"posts", lookup="post")
post_nested_router.register(r"comments", views.CommentViewSet, basename="post-comment")

user_post_nested_router = NestedDefaultRouter(user_nested_router, r"posts", lookup="post")
user_post_nested_router.register(r"comments", views.CommentViewSet, basename="user-post-comment")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(user_nested_router.urls)),
    path("", include(post_nested_router.urls)),
    path("", include(user_post_nested_router.urls)),
    path("me/", views.UserViewSet.as_view({"get": "retrieve"}), name="me-detail"),
    path(
        "me/change_password/",
        lambda request: redirect(request.get_full_path().replace("me", "users"), permanent=True),
        name="redirect-change-password",
    ),
]
