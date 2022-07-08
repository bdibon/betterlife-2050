from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Project, Organization


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        exclude = ('members', 'admins')


class ProjectSerializerAllRights(serializers.ModelSerializer):

    class Meta:
        model = Project
        # Use a dedicated endpoint for members
        exclude = ('members',)


    def validate(self, data):
        owner_pk = data.get('owner')
        organization_pk = data.get('organization')

        if owner_pk and organization_pk:
            members_queryset = Organization.objects.get(pk=organization_pk).members.values_list('pk', flat=True)
            if owner_pk in members_queryset:
                raise ValidationError("Owner must belong to organization")
        return data


class ProjectSerializerProjectOwner(ProjectSerializerAllRights):

    class Meta:
        model = Project
        # Use a dedicated endpoint for members
        exclude = ('members',)
        read_only_fields = ('organization',)


class ProjectSerializerProjectMember(ProjectSerializerProjectOwner):

    class Meta:
        model = Project
        # Use a dedicated endpoint for members
        exclude = ('members',)
        read_only_fields = ('organization', 'title', 'goal', 'owner')


class ProjectSerializerReadOnly(ProjectSerializerProjectMember):

    class Meta:
        model = Project
        # Use a dedicated endpoint for members
        exclude = ('members',)
        read_only_fields = ('organization', 'title', 'goal', 'owner', 'description')
