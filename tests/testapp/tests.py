import unittest
from django.contrib.auth.models import User
from django.contrib import admin
from django.test import RequestFactory
from django.core.exceptions import (
    FieldDoesNotExist,
)

from arbitrary_inline.admin import (
    ArbitraryStackedInline,
    ArbitraryTabularInline,
)
from arbitrary_inline.forms import (
    arbitrary_inlineformset_factory,
    BaseArbitraryInlineFormSet,
)

from .models import (
    Parent,
    Related1,
    Related2,
)
from .admin import (
    Related1InlineForRelated2,
    Related2InlineForRelated1,
)


class ModelInlineTestCase(unittest.TestCase):
    def setUp(self):
        self.admin_site = admin.site
        self.rf = RequestFactory()

    def test_instantiation(self):
        inline_instances = [
            Related1InlineForRelated2(Related2, admin.site),
            Related2InlineForRelated1(Related1, admin.site),
        ]
        for ii in inline_instances:
            request = self.rf.get('/admin/testapp/____/add')
            request.user = User(id=1, username='tester', is_superuser=True)

            formset = ii.get_formset(request)

            request = self.rf.get('/admin/testapp/____/3/')
            request.user = User(id=1, username='tester', is_superuser=True)

            formset = ii.get_formset(request, obj=ii.model(3, "fake name", 5))


class FormSetTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_factory(self):
        with self.assertRaises(FieldDoesNotExist):
            arbitrary_inlineformset_factory(Related1, Related2)
        with self.assertRaises(FieldDoesNotExist):
            arbitrary_inlineformset_factory(
                Related1, Related2, model_field='WRONG',
                parent_model_field='ALSO WRONG'
            )
        with self.assertRaises(FieldDoesNotExist):
            arbitrary_inlineformset_factory(
                Related1, Related2, model_field='r1parent',
                parent_model_field='WRONG'
            )
        with self.assertRaises(FieldDoesNotExist):
            arbitrary_inlineformset_factory(
                Related1, Related2, model_field='WRONG',
                parent_model_field='r2parent'
            )

        formset = arbitrary_inlineformset_factory(
            Related1, Related2, model_field='r1parent',
            parent_model_field='r2parent'
        )
        self.assertTrue(issubclass(formset, BaseArbitraryInlineFormSet))
