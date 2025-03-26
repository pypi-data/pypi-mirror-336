from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from flexi_tag.models import Tag, TaggedItem


@override_settings(ROOT_URLCONF="flexi_tag.urls")
class TagViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.client.force_authenticate(user=self.admin_user)

        self.tag = Tag.objects.create(
            name="test_tag",
        )

        self.list_url = "/tags/"
        self.detail_url = "/tags/" + str(self.tag.id) + "/"

    def test_list_tags(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_tag(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_tag")

    def test_create_tag(self):
        data = {
            "name": "new_tag",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 2)
        self.assertEqual(response.data["name"], "new_tag")

    def test_update_tag(self):
        data = {
            "name": "updated_tag",
        }
        response = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "updated_tag")

    def test_delete_tag(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)

    def test_unauthorized_access(self):
        self.client.force_authenticate(
            user=User.objects.create_user(
                username="regular_user", password="regular123"
            )
        )

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


@override_settings(ROOT_URLCONF="flexi_tag.urls")
class TaggedItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin2", email="admin2@example.com", password="admin123"
        )
        self.client.force_authenticate(user=self.admin_user)

        self.tag = Tag.objects.create(name="test_tag")
        self.content_type = ContentType.objects.create(
            app_label="test_app", model="test_model"
        )
        self.tagged_item = TaggedItem.objects.create(
            tag=self.tag,
            content_type=self.content_type,
            object_id=1,
            name=self.tag.name,
        )

        self.list_url = "/tagged-items/"
        self.detail_url = "/tagged-items/" + str(self.tagged_item.id) + "/"

    def test_list_tagged_items(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_tagged_item(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.tag.name)
        self.assertEqual(response.data["tag_name"], self.tag.name)

    def test_create_tagged_item_not_allowed(self):
        data = {
            "tag": self.tag.id,
            "content_type": self.content_type.id,
            "object_id": 2,
            "name": "test",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorized_access(self):
        self.client.force_authenticate(
            user=User.objects.create_user(
                username="regular_user", password="regular123"
            )
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
