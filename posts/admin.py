from django.contrib import admin
from .models import Post, Image, Comment, Like, Share

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Share)
