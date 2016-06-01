# Arbitrary InlineModelAdmin for Django Admin

[![Build Status](https://travis-ci.org/mediapredict/django_arbitrary_inline.svg?branch=master)](https://travis-ci.org/mediapredict/django_arbitrary_inline)

Normally you would use a model inline in Django Admin to show a model which has
a Foreign Key to the primary model you are editing. In some cases, like when you
have a bunch of other models which point to the same primary model (e.g., 
`auth.User`) you might want to show a handful of the related models on the admin
for your `UserProfile` model even though all of them have a Foreign Key to
`User`. That is now possible.

### Example:

```python
from django.contrib import admin
from arbitrary_inline.admin import ArbitraryTabularInline, ArbitraryStackedInline

from .models import UserProfile, UserNotificationPreference


class UserNotificationPreferenceInline(ArbitraryTabularInline):
    """
    UserProfile and UserNotificationPreference both have a FK to auth.User
    """
    model = UserNotificationPreference
    
    # UserNotificationPreference.pref_user is the FK to auth.User
    model_field = "pref_user"
    
    # UserProfile.django_user is the FK to auth.User
    parent_model_field = "django_user"
    

class UserProfileAdmin(admin.ModelAdmin):
    inlines = [UserNotificationPreferenceInline,]


admin.site.register(UserProfile, UserProfileAdmin)
```

### Installation

```sh
pip install django-abritrary-inline
```

### License

This package is BSD licensed (See LICENSE file). Some of the code is based
on `django.contrib.contenttypes.admin.GenericInlineModelAdmin` (hence the 
mention of Django in the LICENSE file). The Django Software Foundation is not
affiliated with this project or this package.
