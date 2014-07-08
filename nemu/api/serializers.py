__author__ = 'Mateusz'
from rest_framework import serializers
from models import UserProfile, User, Project, ScanlationGroupProjects, Chapter


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('number', 'status')


class ProjectSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(required=False, many=False)
    class Meta:
        model = Project
        fields = ('id', 'title', 'status', 'chapters')


class ScanlationGroupProjectsSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(required=False, many=False)
    class Meta:
        model = ScanlationGroupProjects
        fields = ('project', 'group_id')