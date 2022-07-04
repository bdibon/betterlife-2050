from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action


from projects.models import Organization, Project
from projects.serializers import OrganizationSerializer, ProjectSerializer

from .serializers import CustomUserSerializer



class CustomUserViewSet(ModelViewSet, RetrieveModelMixin, ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer

    @action(methods=['get'], detail=True, url_path="projects")
    def get_projects(self, request, pk=None):
        projects = Project.objects.filter(members__id__in=[pk])
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="owned-projects")
    def get_owned_projects(self, request, pk=None):
        projects = Project.objects.filter(owner=pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="organizations")
    def get_organizations(self, request, pk=None):
        organizations = Organization.objects.filter(members__in=[pk])
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="managed-organizations")
    def get_managed_organizations(self, request, pk=None):
        organizations = Organization.objects.filter(admins__in=[pk])
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)
