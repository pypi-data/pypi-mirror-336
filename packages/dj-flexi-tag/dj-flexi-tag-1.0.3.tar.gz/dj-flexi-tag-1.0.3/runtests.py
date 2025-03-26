#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "flexi_tag.tests.test_settings"
    django.setup()

    verbosity_level = 2

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity_level)
    failures = test_runner.run_tests(["flexi_tag.tests"])
    sys.exit(bool(failures))
