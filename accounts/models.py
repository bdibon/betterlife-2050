from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def is_member_of_an_organization(self):
        return self.organizations.count()

    def belongs_to_organization(self, organization):
        return organization in self.organizations.all() or self in organization.admins.all()

    def is_project_member(self, project):
        return self in project.members.all() or self == project.owner

    def is_project_owner(self, project):
        return self == project.owner

    def is_organization_admin(self, organization):
        return self in organization.admins.all()
