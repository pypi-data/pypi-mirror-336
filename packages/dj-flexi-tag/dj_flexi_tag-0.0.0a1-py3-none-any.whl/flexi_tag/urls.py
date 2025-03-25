try:
    from django.urls import include, path
except ImportError:
    from django.conf.urls import include, url as path

from rest_framework.routers import DefaultRouter

from flexi_tag.resources.views import TaggedItemViewSet, TagViewSet

router = DefaultRouter()
router.register(
    r"tags",
    TagViewSet,
    basename="tags",
)
router.register(
    r"tagged-items",
    TaggedItemViewSet,
    basename="tagged-items",
)

app_name = "flexi_tag"


urlpatterns = [path("", include(router.urls))]
