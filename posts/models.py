from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    caption = models.TextField()
    images = models.ManyToManyField("Image", related_name="photo_post", blank=True)

    def __str__(self) -> str:
        return self.caption



# class PhotoPost(Post):
#     images = models.ManyToManyField("Image", related_name="photo_post")


class Image(models.Model):
    image = models.ImageField(upload_to='posts/images')


