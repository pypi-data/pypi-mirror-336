from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from flexi_tag.exceptions import (
    TagIDRequiredException,
    TagIDsRequiredException,
    TagNotFoundException,
)
from flexi_tag.models import Tag
from flexi_tag.utils.service import TaggableService


class TaggableViewSetMixin(object):
    taggable_service = TaggableService()

    @action(detail=True, methods=["post"])
    def add_tag(self, request, pk=None):
        obj = self.get_object()
        tag_id = request.data.get("tag_id")

        if not tag_id:
            raise TagIDRequiredException()

        tag = Tag.objects.get(id=tag_id)
        if not tag:
            raise TagNotFoundException()

        self.taggable_service.add_tag(obj, tag)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def remove_tag(self, request, pk=None):
        obj = self.get_object()
        tag_id = request.data.get("tag_id")

        if not tag_id:
            raise TagIDRequiredException()

        tag = Tag.objects.get(id=tag_id)
        if not tag:
            raise TagNotFoundException()

        self.taggable_service.remove_tag(obj, tag)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def filter_by_tag(self, request):
        tag_id = request.query_params.get("tag_id")

        if not tag_id:
            raise TagIDRequiredException()

        queryset = self.taggable_service.filter_by_tag(
            queryset=self.get_queryset(),
            tag_id=tag_id,
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def filter_by_tag_name(self, request):
        tag_name = request.query_params.get("tag_name")

        if not tag_name:
            raise TagIDsRequiredException()

        queryset = self.taggable_service.filter_by_tag_name(
            queryset=self.get_queryset(),
            tag_name=tag_name,
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
