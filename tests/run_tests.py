# -*- coding: utf-8 -*-
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


os.chdir(os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
django.setup()


TestRunner = get_runner(settings)
failures = TestRunner().run_tests(sys.argv[2:])

if failures:
    sys.exit(bool(failures))
