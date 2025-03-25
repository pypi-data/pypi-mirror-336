=============
API Reference
=============

Models
======

Tag
---

.. code-block:: python

    class Tag(models.Model):
        """
        The main tag model that stores tag information.
        """
        name = models.CharField(max_length=100)
        slug = models.SlugField(unique=True, max_length=100)
        created_at = models.DateTimeField(auto_now_add=True)

        # Methods
        def get_absolute_url(self):
            """Returns the URL for this tag"""

        def similar_objects(self):
            """Returns objects with similar tags"""

TaggedItem
---------

.. code-block:: python

    class TaggedItem(models.Model):
        """
        Represents the relationship between a tag and the tagged object.
        """
        tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')
        created_at = models.DateTimeField(auto_now_add=True)

Fields
======

TagField
-------

.. code-block:: python

    class TagField(models.CharField):
        """
        A custom field that handles the relationship between a tagged model
        and the Tag model.
        """

        def __init__(self, separator=',', max_tags=None, *args, **kwargs):
            """
            Initialize the TagField.

            Args:
                separator: Character used to separate tags (default: comma)
                max_tags: Maximum number of tags allowed (default: unlimited)
            """

Managers
=======

TagManager
---------

.. code-block:: python

    class TagManager(models.Manager):
        """
        Custom manager for Tag model that provides additional functionality.
        """

        def get_or_create_tags(self, tag_list):
            """
            Takes a list of tag names and returns corresponding Tag objects.
            Creates tags that don't exist.
            """

        def most_common(self, limit=10, min_count=None):
            """
            Returns the most commonly used tags.
            """

        def similar_tags(self, tag, min_correlation=0.1):
            """
            Returns tags that are frequently used together with the given tag.
            """

Utilities
========

.. code-block:: python

    def parse_tags(tag_string, separator=','):
        """
        Parse a string of tags into a list of cleaned tag names.
        """

    def get_tag_cloud(queryset_or_model, min_count=None, steps=4):
        """
        Generate a tag cloud for the given queryset or model.

        Returns tags with a 'font_size' attribute (1-steps) based on frequency.
        """

    def related_objects_by_tags(obj, model_class, min_tags=1):
        """
        Find objects of the given model class that share tags with obj.

        Returns a queryset ordered by number of shared tags.
        """
