from django.db import models
from django.contrib.auth.models import User
import os
from PIL import Image as PilImage


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    caption = models.TextField()
    images = models.ManyToManyField("Image", related_name="photo_post", blank=True)

    def __str__(self) -> str:
        return self.caption
    
    def delete(self, *args, **kwargs):
        self.images.all().delete()
        super().delete(*args, **kwargs)
    

class Image(models.Model):
    image = models.ImageField(upload_to='posts/images')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = PilImage.open(self.image.path)
        max_size = (1053, 569)

        img.thumbnail(max_size, PilImage.ANTIALIAS)

        img.save(self.image.path)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.text}'


class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'author')

    def __str__(self):
        return f'{self.author.username} likes {self.post.caption}'