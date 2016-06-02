from __future__ import unicode_literals

from functools import partial

from django.contrib.admin.checks import InlineModelAdminChecks
from django.contrib.admin.options import InlineModelAdmin, flatten_fieldsets
from .forms import (
    BaseArbitraryInlineFormSet,
    arbitrary_inlineformset_factory,
)
from django.forms import ALL_FIELDS
from django.forms.models import modelform_defines_fields


class ArbitraryInlineModelAdminChecks(InlineModelAdminChecks):
    def _check_exclude_of_parent_model(self, obj, parent_model):
        # There's no FK to exclude, so no exclusion checks are required.
        return []

    def _check_relation(self, obj, parent_model):
        return []


class ArbitraryInlineModelAdmin(InlineModelAdmin):
    formset = BaseArbitraryInlineFormSet
    checks_class = ArbitraryInlineModelAdminChecks

    def get_formset(self, request, obj=None, **kwargs):
        if 'fields' in kwargs:
            fields = kwargs.pop('fields')
        else:
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)
        exclude.extend(self.get_readonly_fields(request, obj))
        if (self.exclude is None
                and hasattr(self.form, '_meta')
                and self.form._meta.exclude):
            # Take the custom ModelForm's Meta.exclude into account only if the
            # GenericInlineModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)
        exclude = exclude or None
        can_delete = (self.can_delete
                      and self.has_delete_permission(request, obj))
        defaults = {
            "model_field": self.model_field,
            "parent_model_field": self.parent_model_field,
            "form": self.form,
            "formfield_callback": partial(self.formfield_for_dbfield,
                                          request=request),
            "formset": self.formset,
            "extra": self.get_extra(request, obj),
            "can_delete": can_delete,
            "can_order": False,
            "fields": fields,
            "min_num": self.get_min_num(request, obj),
            "max_num": self.get_max_num(request, obj),
            "exclude": exclude
        }
        defaults.update(kwargs)

        if (defaults['fields'] is None
                and not modelform_defines_fields(defaults['form'])):
            defaults['fields'] = ALL_FIELDS

        return arbitrary_inlineformset_factory(self.model,
                                               self.parent_model,
                                               **defaults)


class ArbitraryStackedInline(ArbitraryInlineModelAdmin):
    template = 'admin/edit_inline/stacked.html'


class ArbitraryTabularInline(ArbitraryInlineModelAdmin):
    template = 'admin/edit_inline/tabular.html'
