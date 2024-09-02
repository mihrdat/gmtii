from rest_framework_nested import routers
from .views import CategoryViewSet, ContentViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("contents", ContentViewSet)

urlpatterns = router.urls
