from django.contrib import admin
from arbitrary_inline.admin import (
    ArbitraryStackedInline,
    ArbitraryTabularInline,
)
from .models import Related1, Related2


class Related1InlineForRelated2(ArbitraryStackedInline):
    model = Related1
    model_field = 'r1parent'
    parent_model_field = 'r2parent'


class Related2InlineForRelated1(ArbitraryTabularInline):
    model = Related2
    model_field = 'r2parent'
    parent_model_field = 'r1parent'


class Related1Admin(admin.ModelAdmin):
    inlines = [Related2InlineForRelated1]


class Related2Admin(admin.ModelAdmin):
    inlines = [Related1InlineForRelated2]


admin.site.register(Related1, Related1Admin)
admin.site.register(Related2, Related2Admin)
