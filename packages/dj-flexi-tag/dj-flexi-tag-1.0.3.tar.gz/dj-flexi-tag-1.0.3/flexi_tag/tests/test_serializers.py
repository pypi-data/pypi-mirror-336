from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from flexi_tag.models import Tag, TaggedItem
from flexi_tag.resources.serializers import TaggedItemSerializer, TagSerializer


class TagSerializerTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Existing Tag")
        self.serializer = TagSerializer(instance=self.tag)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"name"})

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["name"], "Existing Tag")

    def test_validate_empty_name(self):
        serializer = TagSerializer(data={"name": ""})
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class TaggedItemSerializerTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test Tag")
        self.content_type = ContentType.objects.create(
            app_label="test_app", model="test_model"
        )
        self.tagged_item = TaggedItem.objects.create(
            tag=self.tag,
            content_type=self.content_type,
            object_id=1,
            name=self.tag.name,
        )
        self.serializer = TaggedItemSerializer(instance=self.tagged_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = {"id", "tag", "tag_name", "content_type", "object_id", "name"}
        self.assertEqual(set(data.keys()), expected_fields)

    def test_tag_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data["tag_name"], "Test Tag")

    def test_read_only_fields(self):
        data = {"id": "new_id", "name": "new_name", "tag_name": "new_tag_name"}
        serializer = TaggedItemSerializer(self.tagged_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
