from rest_framework.routers import SimpleRouter

from .views import CustomUserViewSet


router = SimpleRouter()
router.register('', CustomUserViewSet)

urlpatterns = router.urls
