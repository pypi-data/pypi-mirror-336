from django.test import TestCase
from mock import MagicMock, patch
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from flexi_tag.exceptions import (
    TagIDRequiredException,
    TagIDsRequiredException,
    TagNotFoundException,
)
from flexi_tag.models import Tag
from flexi_tag.utils.views import TaggableViewSetMixin


class DummyTaggableViewSet(TaggableViewSetMixin):
    """
    A dummy ViewSet that inherits from TaggableViewSetMixin for testing purposes
    """

    def get_object(self):
        return MagicMock()

    def get_queryset(self):
        return MagicMock()

    def get_serializer(self, *args, **kwargs):
        serializer = MagicMock()
        serializer.data = {"id": 1, "name": "test"}
        return serializer

    def paginate_queryset(self, queryset):
        return None


class TaggableViewSetMixinTestCase(TestCase):
    def setUp(self):
        self.viewset = DummyTaggableViewSet()
        self.factory = APIRequestFactory()

        self.mock_taggable_service = MagicMock()
        self.viewset.taggable_service = self.mock_taggable_service

    def _convert_to_drf_request(self, request):
        """Helper method to convert Django request to DRF Request"""
        return Request(request, parsers=[JSONParser()])

    @patch("flexi_tag.utils.views.Tag.objects.get")
    def test_add_tag_success(self, mock_tag_get):
        mock_tag = MagicMock()
        mock_tag_get.return_value = mock_tag
        django_request = self.factory.post("/", {"tag_id": 1}, format="json")
        request = self._convert_to_drf_request(django_request)

        response = self.viewset.add_tag(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.viewset.taggable_service.add_tag.assert_called_once()

    def test_add_tag_missing_tag_id(self):
        django_request = self.factory.post("/", {}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagIDRequiredException):
            self.viewset.add_tag(request, pk=1)

    @patch("flexi_tag.utils.views.Tag.objects.get", side_effect=Tag.DoesNotExist)
    def test_add_tag_not_found(self, mock_tag_get):
        django_request = self.factory.post("/", {"tag_id": 999}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(Tag.DoesNotExist):
            self.viewset.add_tag(request, pk=1)

    @patch("flexi_tag.utils.views.Tag.objects.get")
    def test_remove_tag_success(self, mock_tag_get):
        mock_tag = MagicMock()
        mock_tag_get.return_value = mock_tag
        django_request = self.factory.post("/", {"tag_id": 1}, format="json")
        request = self._convert_to_drf_request(django_request)

        response = self.viewset.remove_tag(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.viewset.taggable_service.remove_tag.assert_called_once()

    def test_remove_tag_missing_tag_id(self):
        django_request = self.factory.post("/", {}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagIDRequiredException):
            self.viewset.remove_tag(request, pk=1)

    @patch("flexi_tag.utils.views.Tag.objects.get", side_effect=Tag.DoesNotExist)
    def test_remove_tag_not_found(self, mock_tag_get):
        django_request = self.factory.post("/", {"tag_id": 999}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(Tag.DoesNotExist):
            self.viewset.remove_tag(request, pk=1)

    def test_filter_by_tag_success(self):
        django_request = self.factory.get("/?tag_id=1")
        request = self._convert_to_drf_request(django_request)
        filtered_queryset = MagicMock()
        self.mock_taggable_service.filter_by_tag.return_value = filtered_queryset

        response = self.viewset.filter_by_tag(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_taggable_service.filter_by_tag.assert_called_once()

    def test_filter_by_tag_missing_tag_id(self):
        django_request = self.factory.get("/")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagIDRequiredException):
            self.viewset.filter_by_tag(request)

    def test_filter_by_tag_name_success(self):
        django_request = self.factory.get("/?tag_name=test")
        request = self._convert_to_drf_request(django_request)
        filtered_queryset = MagicMock()
        self.mock_taggable_service.filter_by_tag_name.return_value = filtered_queryset

        response = self.viewset.filter_by_tag_name(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mock_taggable_service.filter_by_tag_name.assert_called_once()

    def test_filter_by_tag_name_missing_tag_name(self):
        django_request = self.factory.get("/")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagIDsRequiredException):
            self.viewset.filter_by_tag_name(request)

    @patch("flexi_tag.utils.views.Tag.objects.get")
    def test_add_tag_none_tag(self, mock_tag_get):
        mock_tag_get.return_value = None
        django_request = self.factory.post("/", {"tag_id": 1}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagNotFoundException):
            self.viewset.add_tag(request, pk=1)

    @patch("flexi_tag.utils.views.Tag.objects.get")
    def test_remove_tag_none_tag(self, mock_tag_get):
        mock_tag_get.return_value = None
        django_request = self.factory.post("/", {"tag_id": 1}, format="json")
        request = self._convert_to_drf_request(django_request)

        with self.assertRaises(TagNotFoundException):
            self.viewset.remove_tag(request, pk=1)
