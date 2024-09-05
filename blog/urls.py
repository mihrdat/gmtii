from rest_framework_nested import routers
from .views import CategoryViewSet, ContentViewSet, PublisherViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("contents", ContentViewSet)
router.register("publishers", PublisherViewSet)

urlpatterns = router.urls
