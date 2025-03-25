from django.test import TestCase
from model_mommy import mommy

from flexi_tag.exceptions import TagValidationException
from flexi_tag.models import Tag, TaggedItem
from flexi_tag.service import TagService


class TagServiceTestCase(TestCase):
    def setUp(self):
        self.service = TagService()

    def test_create_instance(self):
        tag_name = "test_tag"
        tag = self.service.create_instance(tag_name)

        self.assertEqual(tag.name, tag_name)

    def test_update_instance(self):
        tag = mommy.make(Tag, name="old_name")
        tagged_item = mommy.make(TaggedItem, tag=tag, name="old_name")

        new_name = "updated_name"
        self.service.update_instance(tag, new_name)

        tag.refresh_from_db()
        self.assertEqual(tag.name, new_name)

        tagged_item.refresh_from_db()
        self.assertEqual(tagged_item.name, new_name)

    def test_delete_instance(self):
        tag = mommy.make(Tag, name="test_tag")

        self.service.delete_instance(tag)
        self.assertEqual(Tag.objects.filter(id=tag.id).count(), 0)

    def test_create_instance_with_duplicate_name(self):
        tag_name = "test_tag"
        mommy.make(Tag, name=tag_name)

        with self.assertRaises(TagValidationException):
            self.service.create_instance(tag_name)

    def test_update_instance_with_duplicate_name(self):
        mommy.make(Tag, name="existing_tag")
        tag_to_update = mommy.make(Tag, name="tag_to_update")

        with self.assertRaises(TagValidationException):
            self.service.update_instance(tag_to_update, "existing_tag")
