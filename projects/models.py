from django.db import models
from django.conf import settings
from django.conf.global_settings import LANGUAGES


class Organization(models.Model):
    AMERICAN_ENGLISH = "en"
    LANGUAGE_CHOICES = LANGUAGES

    name = models.CharField(max_length=255)
    description = models.TextField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="organizations")
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managed_organizations")
    language = models.CharField(max_length=7, choices=LANGUAGE_CHOICES, default=AMERICAN_ENGLISH)

    def __str__(self):
        return self.name


class Project(models.Model):
    NO_POVERTY = 'NP'
    GOAL_CHOICES = [
        (NO_POVERTY, 'No poverty'),
        ('ZH', 'Zero hunger'),
        ('GHWB', 'Good health and well-being'),
        ('QE', 'Quality education'),
        ('GE', 'Gender equality'),
        ('CWS', 'Clean water and sanitation'),
        ('ACE', 'Affordable and clean energy'),
        ('DWEG', 'Decent work and economic growth'),
        ('III', 'Industry, innovation, and infrastructure'),
        ('RI', 'Reduces inequalities'),
        ('SCC', 'Sustainable cities and communities'),
        ('RCP', 'Responsible consumption & production'),
        ('CA', 'Climate action'),
        ('LW', 'Life below water'),
        ('LL', 'Life on land'),
        ('PJSI', 'Peace, justice, and strong institutions'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    goal = models.CharField(max_length=4, choices=GOAL_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")
    organization = models.ForeignKey("Organization", on_delete=models.PROTECT)


    #############################
    #        Permissions        #
    #############################


    @staticmethod
    def has_read_permission(request):
        # Projects will be filtered at the viewset level
        return True

    def has_object_retrieve_permission(self, request):
        user = request.user
        project_organization = self.organization
        return user.belongs_to_organization(project_organization)

    @staticmethod
    def has_create_permission(request):
        user = request.user
        organization_pk = request.data.get('organization', None)

        if organization_pk is None:
            return False

        if user.is_superuser:
            return True
        if not user.belongs_to_organization(Organization.objects.get(pk=organization_pk)):
            return False
        return True

    def has_object_update_permission(self, request):
        user = request.user

        if user.is_superuser:
            return True

        project_organization = self.organization
        if user.is_organization_admin(project_organization):
            return True

        if user.is_project_owner(self):
            return True

        if user.is_project_member(self):
            return True
        return False

    @staticmethod
    def has_update_permission(request):
        return True

    @staticmethod
    def has_get_members_permission(request):
        return True

    def has_object_get_members_permission(self, request):
        user = request.user

        return user.belongs_to_organization(self.organization) or user.is_superuser

    def __str__(self):
        return self.title
