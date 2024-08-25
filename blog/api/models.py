from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey("auth.User", related_name="post_create_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey("auth.User", related_name="post_changed_by", on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey("auth.User", related_name="comment_create_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey("auth.User", related_name="comment_changed_by", on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment on {self.post.title} by {self.id}"
