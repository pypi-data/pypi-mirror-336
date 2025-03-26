from rest_framework import serializers

from flexi_tag.models import Tag, TaggedItem


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)
        read_only_fields = (
            "id",
            "modified_date",
            "created_date",
        )


class TaggedItemSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source="tag.name", read_only=True)

    class Meta:
        model = TaggedItem
        fields = ("id", "tag", "tag_name", "content_type", "object_id", "name")
        read_only_fields = ("id", "name", "tag_name")
