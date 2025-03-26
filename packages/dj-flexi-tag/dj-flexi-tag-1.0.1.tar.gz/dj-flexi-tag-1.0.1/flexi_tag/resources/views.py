from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from flexi_tag.models import Tag, TaggedItem
from flexi_tag.resources.serializers import TaggedItemSerializer, TagSerializer
from flexi_tag.service import TagService


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    service = TagService()
    ordering_fields = "__all__"
    filterset_fields = ["name"]
    tag_service = TagService()
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.instance = self.tag_service.create_instance(
            name=serializer.validated_data.get("name"),
        )

    def perform_update(self, serializer):
        serializer.instance = self.tag_service.update_instance(
            instance=serializer.instance,
            name=serializer.validated_data.get("name"),
        )

    def perform_destroy(self, instance):
        self.tag_service.delete_instance(instance)


class TaggedItemViewSet(ReadOnlyModelViewSet):
    queryset = TaggedItem.objects.all()
    serializer_class = TaggedItemSerializer
    permission_classes = (IsAdminUser,)
    ordering_fields = "__all__"
    filterset_fields = ["tag", "content_type", "object_id", "name"]
