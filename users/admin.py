from django.contrib import admin
from .models import Profile, Notification, FriendRequest


admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(FriendRequest)
