from django import forms
from warehouse.models import DeviceType, Device


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź urządzenie"}),
    )


class DeviceTypeSearchForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź kategorię"}),
    )


class DeviceTypeForm(forms.Form):
    device_type = forms.ModelChoiceField(
        queryset=DeviceType.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Typ urządzenia",
    )


class DeviceCreateForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ("name", "quantity", "device_type")
        labels = {
            "name": "Nazwa urządzenia",
            "quantity": "Ilość",
            "device_type": "Typ urządzenia",
        }


class DeviceTypeCreateForm(forms.ModelForm):
    class Meta:
        model = DeviceType
        fields = ("name", )
        labels = {
            "name": "Nazwa",
        }

