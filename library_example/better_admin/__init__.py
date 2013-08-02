from django import forms
from tekextensions.widgets import SelectWithPopUp, MultipleSelectWithPopUp


forms.ModelChoiceField.widget = SelectWithPopUp
forms.ModelMultipleChoiceField.widget = MultipleSelectWithPopUp