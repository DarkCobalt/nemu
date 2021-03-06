__author__ = 'Mateusz'
from rest_framework import serializers
from models import UserProfile, User, Project, ScanlationGroupProjects, Chapter, Assigned, RoleInAssigned


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('gg', 'skype', 'opis', 'group_id',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False, many=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ('id', 'number', 'status')


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


class AssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assigned
        fields = ('project_id', 'chapter_id', 'user_id')


class RoleInAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleInAssigned
        fields = ('project_id', 'role')