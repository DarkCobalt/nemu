from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import generics, permissions
from serializers import UserSerializer, ProjectSerializer, ScanlationGroupProjectsSerializer, ChapterSerializer
from .models import User, UserProfile, Project, ScanlationGroupProjects, Chapter


class OnePageAppView(TemplateView):
    template_name = 'api/index.html'


class UserList(generics.ListCreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'


class ProjectList(generics.ListCreateAPIView):
    model = ScanlationGroupProjects
    serializer_class = ScanlationGroupProjectsSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ProjectDetail(generics.RetrieveAPIView):
    model = Project
    serializer_class = ProjectSerializer
    lookup_field = 'title'
    permission_classes = [
        permissions.AllowAny
    ]