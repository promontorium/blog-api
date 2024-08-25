from django.urls import path

from .views import CommentDetail, CommentListView, PostDetail, PostListView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/<int:pk>", PostDetail.as_view(), name="post-detail"),
    path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="post-comments"),
    path("posts/<int:post_id>/comments/<int:pk>", CommentDetail.as_view(), name="post-comment-detail"),
    # ...
    # path("comments/", CommentListView.as_view(), name="comments"),
    # path("comments/<int:pk>", CommentDetail.as_view(), name="comment-detail"),
]
