from django.db import models
from manga.models import Project, Chapter
from django.contrib.auth.models import User


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