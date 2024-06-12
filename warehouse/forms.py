from django import forms
from warehouse.models import DeviceType


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź urządzenie"}),
    )


class DeviceTypeForm(forms.Form):
    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Typ urządzenia",
    )
