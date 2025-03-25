from flexi_tag.models import Tag, TaggedItem


class TaggableService:
    @staticmethod
    def add_tag(instance, tag):
        TaggedItem.objects.create(tag=tag, content_object=instance, name=tag.name)

    @staticmethod
    def remove_tag(instance, tag):
        TaggedItem.objects.filter(tag=tag, content_object=instance).delete()

    @staticmethod
    def get_tags(instance):
        return Tag.objects.filter(
            tagged_items__content_object=instance,
        )

    @staticmethod
    def filter_by_tag(queryset, tag_id):
        return queryset.filter(tagged_items__tag_id=tag_id)

    @staticmethod
    def filter_by_tag_name(queryset, tag_name):
        return queryset.filter(tagged_items__name=tag_name)
