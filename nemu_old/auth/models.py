from django.db import models
from django.contrib.auth.models import User
from manga.models import Project


class ScanlationGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class ScanlationGroupProjects(models.Model):
    group_id = models.ManyToManyField(ScanlationGroup)
    project = models.ManyToManyField(Project)


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    gg = models.CharField(max_length=30, blank=True)
    skype = models.CharField(max_length=30, blank=True)
    opis = models.TextField(max_length=255, blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    group_id = models.ForeignKey(ScanlationGroup, null=True, blank=True)

    def __unicode__(self):
        return "Profil: %s" % self.user


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)
