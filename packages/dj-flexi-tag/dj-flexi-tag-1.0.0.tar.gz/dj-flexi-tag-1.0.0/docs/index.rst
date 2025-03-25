=============
dj-flexi-tag
=============

A flexible tagging system for Django.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   configuration
   contributing

Introduction
===========

dj-flexi-tag provides a versatile and customizable tagging solution for Django projects. It allows developers to implement tagging functionality with flexibility for various use cases.

Features
========

* Flexible tag structures
* Support for multiple tagging models
* Easy integration with existing Django models
* Custom tag fields and validations
* Comprehensive API for tag management
* Django admin integration

Quick Start
==========

.. code-block:: python
    from rest_framework import viewsets
    from dj_flexi_tag.utils.viewset import TaggableViewSetMixin


    class DummyTaggableViewSet(viewsets.ModelViewSet, TaggableViewSetMixin):
        ...
