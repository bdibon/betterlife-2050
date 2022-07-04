from rest_framework import routers

from .views import OrganizationViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('organizations', OrganizationViewSet)

urlpatterns = router.urls
