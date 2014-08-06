"""
Global Filed for Wild Card support using Regex
"""
import fnmatch

from django import forms
from django.core.exceptions import ValidationError


class GlobField(forms.CharField):

    """
    Django does not support lookup type based on
    [Glob](http://bit.ly/JkSbRZ). As a result, there
    is no ready-made solution for providing wildcard
    support in search and filter forms to users who
    are uninterested in investing some time in regex.

    GlobField does just that. It allows the user to
    enter queries like:

    1. Ca? - Matches Cat as well as Car
    2. Do* - Matches Dog as well as Doll
    3. A?s* - Matches Also, Arsenal etc.

    Usage: ::

        >>> from django import forms
        >>> class MyForm(forms.Form):
        ...   glob = GlobField()
        ...
        >>> form = MyForm()
        >>> form = MyForm(data={'glob':'Ca?'})
        >>> form.is_valid()
        True

    """
    def clean(self, value):
        """Uses fnmatch to convert globs to regex -
        which is one of the supported look-up types
        for queries in django.
        """
        if value:
            try:
                return r'^' + fnmatch.translate(value).split("(?ms)")[0].strip('\\Z') + '$'
            except:
                raise ValidationError('Some Error')
        else:
            return value
