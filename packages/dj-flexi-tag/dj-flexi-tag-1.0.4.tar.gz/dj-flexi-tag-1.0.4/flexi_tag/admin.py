from django.contrib import admin

from flexi_tag.models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_date",
        "modified_date",
    )


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tag",
        "content_type",
        "object_id",
        "name",
        "created_date",
        "modified_date",
    )
