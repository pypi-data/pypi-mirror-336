from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet
from django.test import TestCase
from mock import MagicMock, patch

from flexi_tag.models import Tag
from flexi_tag.utils.service import TaggableService


class TaggableServiceTestCase(TestCase):
    def setUp(self):
        self.tag1 = Tag.objects.create(name="test-tag-1")
        self.tag2 = Tag.objects.create(name="test-tag-2")

        self.instance = MagicMock()
        self.instance.pk = 1
        self.instance._meta = MagicMock()
        self.instance._meta.app_label = "test_app"
        self.instance._meta.model_name = "test_model"

        self.content_type = ContentType.objects.get_or_create(
            app_label=self.instance._meta.app_label,
            model=self.instance._meta.model_name,
        )[0]

        self.service = TaggableService()

        self.queryset = MagicMock(spec=QuerySet)

    @patch("flexi_tag.models.TaggedItem.objects.create")
    def test_add_tag(self, mock_create):
        self.service.add_tag(self.instance, self.tag1)

        mock_create.assert_called_once_with(
            tag=self.tag1, content_object=self.instance, name=self.tag1.name
        )

    @patch("flexi_tag.models.TaggedItem.objects.filter")
    def test_remove_tag(self, mock_filter):
        mock_queryset = MagicMock()
        mock_filter.return_value = mock_queryset

        self.service.remove_tag(self.instance, self.tag1)

        mock_filter.assert_called_once_with(tag=self.tag1, content_object=self.instance)
        mock_queryset.delete.assert_called_once()

    @patch("flexi_tag.models.Tag.objects.filter")
    def test_get_tags(self, mock_filter):
        expected_result = MagicMock(spec=QuerySet)
        mock_filter.return_value = expected_result

        result = self.service.get_tags(self.instance)

        mock_filter.assert_called_once_with(tagged_items__content_object=self.instance)
        self.assertEqual(result, expected_result)

    def test_filter_by_tag(self):
        self.service.filter_by_tag(self.queryset, self.tag1.id)

        self.queryset.filter.assert_called_once_with(tagged_items__tag_id=self.tag1.id)

    def test_filter_by_tag_name(self):
        tag_name = "test-tag-1"
        self.service.filter_by_tag_name(self.queryset, tag_name)

        self.queryset.filter.assert_called_once_with(tagged_items__name=tag_name)
