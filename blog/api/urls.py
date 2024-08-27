from django.shortcuts import redirect
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")

user_router = NestedDefaultRouter(router, r"users", lookup="user")
user_router.register(r"posts", views.PostViewSet, basename="user-post")
user_router.register(r"comments", views.CommentViewSet, basename="user-comment")

post_router = NestedDefaultRouter(router, r"posts", lookup="post")
post_router.register(r"comments", views.CommentViewSet, basename="post-comment")

user_post_router = NestedDefaultRouter(user_router, r"posts", lookup="post")
user_post_router.register(r"comments", views.CommentViewSet, basename="user-post-comment")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(user_router.urls)),
    path("", include(post_router.urls)),
    path("", include(user_post_router.urls)),
    path(
        "me/change_password/",
        lambda request: redirect(request.get_full_path().replace("me", "users"), permanent=True),
        name="redirect-change-password",
    ),
]
