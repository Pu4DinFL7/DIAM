from django.contrib.auth.models import User
from django.db import models

class Image(models.Model):
    image = models.ImageField(null=True)
    name = models.CharField(null=True, max_length=200)
    description = models.CharField(max_length=20000)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    bookmark = models.BooleanField(default=False)
    pub_date = models.DateTimeField('Pub_Date', null=True)

    def __str__(self):
        return self.name

class Rats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil_image = models.ImageField(null=True, blank=True)


class Comment(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null = True)
    user = models.ForeignKey(Rats, on_delete=models.CASCADE, null = True)
    comment_text = models.CharField(max_length=20000)
    comment_data = models.DateTimeField('Comment Date')
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.comment_text


class LikedGames(models.Model):
    class Meta:
        unique_together = (('user', 'image'),)
    user = models.ForeignKey(Rats, on_delete=models.CASCADE, null = True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)

class BookmarkImage(models.Model):
    class Meta:
        unique_together = (('user', 'image'),)
    user = models.ForeignKey(Rats, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)