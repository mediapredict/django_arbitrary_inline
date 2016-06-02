from __future__ import unicode_literals

from django.forms import ModelForm, modelformset_factory
from django.forms.models import BaseModelFormSet


class BaseArbitraryInlineFormSet(BaseModelFormSet):
    """
    A formset for generic inline objects to a parent.
    """

    def __init__(self, data=None, files=None, instance=None, save_as_new=None,
                 prefix=None, queryset=None, **kwargs):
        opts = self.model._meta
        self.instance = instance
        self.rel_name = '-'.join((
            opts.app_label, opts.model_name,
            self.model_field.name,
        ))
        if self.instance is None or self.instance.pk is None:
            qs = self.model._default_manager.none()
        else:
            if queryset is None:
                queryset = self.model._default_manager
            shared_val = getattr(self.instance, self.parent_model_field.name)
            qs = queryset.filter(**{self.model_field.name: shared_val})
        super(BaseArbitraryInlineFormSet, self).__init__(
            queryset=qs, data=data, files=files,
            prefix=prefix,
            **kwargs
        )

    @classmethod
    def get_default_prefix(cls):
        opts = cls.model._meta
        return '-'.join((
            opts.app_label, opts.model_name,
            cls.model_field.name,
        ))

    def save_new(self, form, commit=True):
        parent_model_val = getattr(
            self.instance,
            self.parent_model_field.get_attname()
        )
        setattr(
            form.instance,
            self.model_field.get_attname(),
            parent_model_val
        )
        return form.save(commit=commit)


def arbitrary_inlineformset_factory(
        model, parent_model, form=ModelForm,
        formset=BaseArbitraryInlineFormSet, model_field=None,
        parent_model_field=None, fields=None, exclude=None, extra=3,
        can_order=False, can_delete=True, max_num=None,
        formfield_callback=None, validate_max=False, min_num=None,
        validate_min=False):
    """
    Returns a ``BaseArbitraryInlineFormSet`` for the given kwargs.
    """
    opts = model._meta
    parent_opts = parent_model._meta
    # if fields are missing let the error propagate
    model_field = opts.get_field(model_field)

    # let the exception propagate
    parent_model_field = parent_opts.get_field(parent_model_field)
    if exclude is not None:
        exclude = list(exclude)
        exclude.extend([model_field.name])
    else:
        exclude = [model_field.name]
    FormSet = modelformset_factory(model, form=form,
                                   formfield_callback=formfield_callback,
                                   formset=formset, extra=extra,
                                   can_delete=can_delete, can_order=can_order,
                                   fields=fields, exclude=exclude,
                                   max_num=max_num, validate_max=validate_max,
                                   min_num=min_num, validate_min=validate_min)
    FormSet.model_field = model_field
    FormSet.parent_model_field = parent_model_field
    return FormSet
