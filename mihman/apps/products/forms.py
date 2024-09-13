from django import forms
from .models import Category, Subcategory

class SearchForm(forms.Form):
    search = forms.CharField(required=False, label='Search')

class FilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Category'
    )
    subcategory = forms.ModelChoiceField(
        queryset=Subcategory.objects.all(),
        required=False,
        label='Subcategory'
    )