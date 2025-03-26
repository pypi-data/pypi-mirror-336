from flexi_tag.exceptions import TagValidationException
from flexi_tag.models import Tag


class TagService:
    @staticmethod
    def create_instance(name):
        if Tag.objects.filter(name=name).exists():
            raise TagValidationException(name=name)

        return Tag.objects.create(
            name=name,
        )

    @staticmethod
    def update_instance(instance, name):
        if Tag.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise TagValidationException(name=name)

        if instance.tagged_items.exists():
            instance.tagged_items.update(name=name)

        instance.name = name
        instance.save(update_fields=["name"])
        return instance

    @staticmethod
    def delete_instance(instance):
        instance.delete()
