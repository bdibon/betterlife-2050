from django.urls import path
from rest_framework import routers


from .views import (
    OrganizationViewSet,
    ProjectViewSet,
    get_organization_projects,
    get_organization_members,
    get_organization_admins
)

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('organizations', OrganizationViewSet)

urlpatterns = router.urls
urlpatterns += [
    path('organizations/<int:pk>/projects/', get_organization_projects),
    path('organizations/<int:pk>/members/', get_organization_members),
    path('organizations/<int:pk>/admins/', get_organization_admins),
]
