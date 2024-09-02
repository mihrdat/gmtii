from rest_framework_nested import routers
from .views import CategoryViewSet, VideoViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("videos", VideoViewSet)

urlpatterns = router.urls
