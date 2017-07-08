from django.db import models
from uuid import uuid4
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(blank=False, max_length=15)
    owner = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        ret = u"{name} ({owner})".format(name=self.name, owner=self.owner.username)
        return ret

    def __str__(self):
        ret = "{name} ({owner})".format(name=self.name, owner=self.owner.username)
        return ret


class Task(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    title = models.CharField(blank=False, max_length=128)
    category = models.ForeignKey(Category)
    description = models.TextField(blank=False)
    sort_weight = models.PositiveIntegerField(default=0, blank=False)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        ret = u"{title} ({owner})".format(title=self.title, owner=self.category.owner.username)
        return ret

    def __str__(self):
        ret = "{title} ({owner})".format(title=self.title, owner=self.category.owner.username)
        return ret


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)