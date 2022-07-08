from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from dry_rest_permissions.generics import DRYPermissions


from accounts.serializers import CustomUserSerializer

from .models import Project, Organization
from .serializers import (
    ProjectSerializerAllRights,
    ProjectSerializerProjectOwner,
    ProjectSerializerProjectMember,
    ProjectSerializerReadOnly,
    OrganizationSerializer
)


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
# @permission_classes([OrganizationMemberOnly])
def get_organization_projects(request, pk):
    projects = Project.objects.filter(organization__id=pk)
    serializer = ProjectSerializerReadOnly(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([OrganizationMemberOnly])
def get_organization_members(request, pk):
    members = get_user_model().objects.filter(organizations__in=[pk])
    serializer = CustomUserSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([OrganizationMemberOnly])
def get_organization_admins(request, pk):
    admins = get_user_model().objects.filter(managed_organizations__in=[pk])
    serializer = CustomUserSerializer(admins, many=True)
    return Response(serializer.data)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializerReadOnly
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return self.queryset
        return self.queryset.filter(organization__in=user.organizations.all())

    def get_serializer_class(self):
        user = self.request.user

        if user.is_superuser or self.action == 'create':
            return ProjectSerializerAllRights
        if self.action == 'update' or self.action == 'partial_update':
            project_pk = int(self.kwargs.get(self.lookup_field))
            project = Project.objects.get(pk=project_pk)
            if user.is_project_owner(project) or user.is_organization_admin(project.organization):
                return ProjectSerializerProjectOwner
            return ProjectSerializerProjectMember
        return ProjectSerializerReadOnly

    @action(methods=['get'], detail=True, url_path="members")
    def get_members(self, request, pk=None):
        project = self.get_object()
        self.check_object_permissions(request, project)
        members = get_user_model().objects.filter(projects__in=[pk])
        serializer = CustomUserSerializer(members, many=True)
        return Response(serializer.data)
