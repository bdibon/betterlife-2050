from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response


from accounts.serializers import CustomUserSerializer

from .models import Project, Organization
from .serializers import ProjectSerializer, OrganizationSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(methods=['get'], detail=True, url_path="projects")
    def get_projects(self, request, pk=None):
        projects = Project.objects.filter(organization__id=pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="members")
    def get_members(self, request, pk=None):
        members = get_user_model().objects.filter(organizations__in=[pk])
        serializer = CustomUserSerializer(members, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path="admins")
    def get_admins(self, request, pk=None):
        admins = get_user_model().objects.filter(managed_organizations__in=[pk])
        serializer = CustomUserSerializer(admins, many=True)
        return Response(serializer.data)

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(methods=['get'], detail=True, url_path="members")
    def get_members(self, request, pk=None):
        members = get_user_model().objects.filter(projects__in=[pk])
        serializer = CustomUserSerializer(members, many=True)
        return Response(serializer.data)
