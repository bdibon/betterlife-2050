from django.db import models
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.forms import ValidationError


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
    goal = models.CharField(max_length=4, choices=GOAL_CHOICES, default=NO_POVERTY)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects")
    organization = models.ForeignKey("Organization", on_delete=models.PROTECT)

    def __str__(self):
        return self.title


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
