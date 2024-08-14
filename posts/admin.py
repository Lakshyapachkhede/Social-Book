from django.contrib import admin
from .models import Post, Image, Comment, Like

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
