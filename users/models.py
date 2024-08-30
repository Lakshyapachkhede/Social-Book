from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import os
from PIL import Image as PilImage



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intro = models.CharField(max_length=100, blank=True)
    banner_image = models.ImageField(default="default-banner.jpg", upload_to="profile_pics/banner")
    user_image = models.ImageField(default="default.png", upload_to="profile_pics/user_image")
    works = models.CharField(blank=True, max_length=50)
    education = models.CharField(blank=True, max_length=50)
    home = models.CharField(blank=True, max_length=50)
    location = models.CharField(blank=True, max_length=50)

    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="friends_with")

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def save(self, *args, **kwargs):
        if self.pk:
            old_profile_image = Profile.objects.get(pk=self.pk).user_image
            old_banner_image = Profile.objects.get(pk=self.pk).banner_image
            
            if old_profile_image != self.user_image and old_profile_image != 'default.png':
                if os.path.isfile(old_profile_image.path):
                    os.remove(old_profile_image.path)

            if old_banner_image != self.banner_image and old_banner_image != 'default-banner':
                if os.path.isfile(old_banner_image.path):
                    os.remove(old_banner_image.path)

        super().save(*args, **kwargs)

        profile_image = PilImage.open(self.user_image.path)
        if profile_image.height > 300:
            output_size = (292, 292)
            profile_image.thumbnail(output_size)
            profile_image.save(self.user_image.path)

        banner_image = PilImage.open(self.banner_image.path)
        if banner_image.height > 600:
            output_size = (1905, 601)
            banner_image.thumbnail(output_size)
            banner_image.save(self.banner_image.path)

    
    def add_friend(self, profile):
        """Send a friend request to another user."""
        friend_request = FriendRequest.objects.create(from_user=self.user, to_user=profile.user)
        return friend_request
    
    def remove_friend(self, profile):
        """Remove a friend."""
        self.friends.remove(profile)
        profile.friends.remove(self)

    def get_friends(self):
        """Returns list of all friends"""
        return self.friends.all()
    
    def get_friend_requests(self):
        """Return a list of all friend requests received."""
        return self.user.friend_requests_received.filter(is_active=True)

    def get_sent_requests(self):
        """Return a list of all friend requests sent."""
        return self.user.friend_requests_sent.filter(is_active=True)
    

    def mutual_friends(self, other_profile):
        return self.friends.filter(id__in=other_profile.friends.values_list('id', flat=True)).count()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name="friends_requests_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friends_requests_received", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def accept(self):
        """"Accept a friend request"""
        self.to_user.profile.friends.add(self.from_user.profile)
        self.from_user.profile.friends.add(self.to_user.profile)
        self.delete()

    def reject(self):
        """"Rejects a friend Request"""
        self.delete()

    def cancel(self):
        """cancels a friend request"""
        self.delete()

    def __str__(self):
        return f"request from {self.from_user.username} to {self.to_user.username}"


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('FR', 'Friend Request'),
        ('AC', 'Accepted Friend Request'),
        ('RJ', 'Rejected Friend Request'),
        ('CM', 'Comment'),
        ('LK', 'Like'),
    )

    sender = models.ForeignKey(User, related_name="sent_notifications", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_notifications", on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"notification from {self.sender} to {self.receiver} - {self.notification_type}"
    







