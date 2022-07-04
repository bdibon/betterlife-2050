from rest_framework import serializers

from .models import Project, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('members', 'admins')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ('members',)
