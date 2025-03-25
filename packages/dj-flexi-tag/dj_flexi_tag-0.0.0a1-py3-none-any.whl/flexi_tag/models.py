import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class StarterModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        update_fields = kwargs.pop("update_fields", None)
        if update_fields is not None:
            if not isinstance(update_fields, list):
                update_fields = list(update_fields)
            update_fields.append("modified_date")
            kwargs["update_fields"] = update_fields
        super(StarterModel, self).save(*args, **kwargs)


class Tag(StarterModel):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class TaggedItem(StarterModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="tagged_items")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    name = models.CharField(
        max_length=255, db_index=True
    )  # This field fills from Tag's name

    class Meta:
        unique_together = (
            "tag",
            "content_type",
            "object_id",
        )
