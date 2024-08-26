from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_posts", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, related_name="changed_posts", null=True, on_delete=models.DO_NOTHING)
    changed_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comment_post", on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_comments", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, related_name="changed_comments", null=True, on_delete=models.DO_NOTHING)
    changed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Comment on {self.post.title} by {self.id}"
