from rest_framework_nested import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet)

urlpatterns = router.urls
