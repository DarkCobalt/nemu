from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import generics, permissions
from serializers import UserSerializer, ProjectSerializer, ScanlationGroupProjectsSerializer, AssignedSerializer, RoleInAssignedSerializer
from .models import User, UserProfile, Project, ScanlationGroupProjects, Chapter, Assigned, RoleInAssigned


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)  # Lookup the object


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



class AssignedDetail(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    model = Assigned
    serializer_class = AssignedSerializer
    lookup_fields = ('project_id', 'chapter_id')
    permission_classes = [
        permissions.AllowAny
    ]