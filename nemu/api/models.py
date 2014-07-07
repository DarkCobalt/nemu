from django.db import models
from django.contrib.auth.models import User


class ScanlationGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='profile')
    gg = models.CharField(max_length=30, blank=True)
    skype = models.CharField(max_length=30, blank=True)
    opis = models.TextField(max_length=255, blank=True)
    avatar = models.CharField(max_length=255, blank=True)
    group_id = models.ForeignKey(ScanlationGroup, to_field='name', related_name='scanlationgroup', null=True, blank=True)

    def __unicode__(self):
        return "Profil: %s" % self.user


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


class MangaStatus(models.Model):
    manga_status = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.manga_status


class ChapterStatus(models.Model):
    chapter_status = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.chapter_status


class Project(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.ForeignKey(MangaStatus, to_field='manga_status')

    def __unicode__(self):
        return self.title


class Chapter(models.Model):
    project = models.ForeignKey(Project, to_field='title', related_name='chapters')
    status = models.ManyToManyField(ChapterStatus)
    number = models.CharField(max_length=10)

    def display_status(self):
        return ','.join([ChapterStatus.chapter_status for ChapterStatus in self.status.all()])

    display_status.short_description = 'Status'
    display_status.allow_tags = True

    def __unicode__(self):
        return self.number


class ScanlationGroupProjects(models.Model):
    group_id = models.ManyToManyField(ScanlationGroup)
    project = models.ManyToManyField(Project, related_name='project')


class Role(models.Model):
    role = models.CharField(max_length=15, unique=True)

    def __unicode__(self):
        return self.role


class Assigned(models.Model):
    user_id = models.ManyToManyField(User, null=True)
    project_id = models.ForeignKey(Project)
    chapter_id = models.ForeignKey(Chapter)

    def display_user(self):
        return ','.join([User.username for User in self.user_id.all()])

    display_user.short_description = 'Users'
    display_user.allow_tags = True

    def __unicode__(self):
        return unicode(self.project_id)


class RoleInAssigned(models.Model):
    project_id = models.ForeignKey(Assigned, null=True)
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return unicode(self.project_id)
