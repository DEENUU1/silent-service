from django import forms
from workshop.models import RepairItem


class SearchForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź klienta"}),
    )


class SearchRepairItemForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź zlecenie"}),
    )


class RepairItemStatusForm(forms.Form):
    status = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = "Zlecenie zakończone"


class RepairItemPriorityForm(forms.Form):
    PRIORITY = (
        ("low", "Niski"),
        ("medium", "Średni"),
        ("high", "Wysoki"),
    )

    priority = forms.ChoiceField(choices=PRIORITY, required=False)
