# Django Flexi Tag

[![Build status](https://img.shields.io/bitbucket/pipelines/akinonteam/dj-flexi-tag)](https://bitbucket.org/akinonteam/dj-flexi-tag/addon/pipelines/home)
[![Documentation status](https://readthedocs.org/projects/dj-flexi-tag/badge/?version=latest)](https://dj-flexi-tag.readthedocs.io/en/latest/?badge=latest)
![PyPI](https://img.shields.io/pypi/v/dj-flexi-tag)
![PyPI - Django version](https://img.shields.io/pypi/djversions/dj-flexi-tag)
![PyPI - Python version](https://img.shields.io/pypi/pyversions/dj-flexi-tag)
![PyPI - License](https://img.shields.io/badge/License-MIT-green.svg)

Flexi tag informs subscribed users via an URL when a specific event occurs.

## Installation

Installation using pip:

```
pip install dj-flexi-tag
```

`flexi-tag` package has to be added to `INSTALLED_APPS` and `migrate` command has to be run.

```python
INSTALLED_APPS = (
    # other apps here...
    'flexi_tag',
)
```
After that, need to add to show Tag and TaggedItem in ModelViewSet.
```python
urlpatterns = [
...
    re_path(
        r'^v1/whisperer/',
        include('flexi_tag.urls', namespace='flexi_tag')
    ),
...
]
```

So, Implementation to the desired ModelViewSet is done as follows;
```python
    from rest_framework import viewsets
    from dj_flexi_tag.utils.viewset import TaggableViewSetMixin


    class DummyTaggableViewSet(viewsets.ModelViewSet, TaggableViewSetMixin):
    ...
```
