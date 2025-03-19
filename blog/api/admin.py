from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Comment, Post, User

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User, UserAdmin)
