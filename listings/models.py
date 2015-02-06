from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    last_online = models.DateTimeField(default=datetime.date(2000, 1, 1))

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    profile = models.ForeignKey(Profile, related_name='favorites')
    post_id = models.IntegerField(default=0)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=200, default="")
    content = models.CharField(max_length=10000, default="")
    create_date = models.DateTimeField(default=datetime.date(2000, 1, 1))
    expiry_date = models.DateTimeField(default=datetime.date(2000, 1, 1))
    views = models.IntegerField(default=0)
    location = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    GENERAL = 'general'
    FORSALE = 'forsale'
    SERVICES = 'services'
    HOUSING = 'housing'
    CATEGORIES = (
        (None, 'Select a category'),
        (GENERAL, 'General'),
        (FORSALE, 'For Sale'),
        (SERVICES, 'Services'),
        (HOUSING, 'Housing'),
    )
    category = models.CharField(max_length=2, choices=CATEGORIES, default=GENERAL)

    def __str__(self):
        return self.title


class Picture(models.Model):
    post = models.ForeignKey(Post, related_name='pictures')
    file = ImageField(upload_to='listing_images/%Y/%m/%d', default="")
    title = models.CharField(max_length=50, default="")
    upload_date = models.DateField('Uploaded On')
    position = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.file.url


class Tag(models.Model):
    posts = models.ManyToManyField(Post, related_name='tags')
    description = models.CharField("Tag", max_length=50, default="")

    def __str__(self):
        return self.description