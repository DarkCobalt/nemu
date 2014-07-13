from django.db import models


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
    project = models.ForeignKey(Project)
    status = models.ManyToManyField(ChapterStatus)
    number = models.CharField(max_length=10)

    def display_status(self):
        return ','.join([ChapterStatus.chapter_status for ChapterStatus in self.status.all()])

    display_status.short_description = 'Status'
    display_status.allow_tags = True

    def __unicode__(self):
        return self.number