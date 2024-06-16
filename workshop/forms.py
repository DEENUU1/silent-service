from django import forms
from workshop.models import Customer, RepairItem


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


class RepairItemCreateForm(forms.ModelForm):
    serial_number = forms.CharField(max_length=100, required=True, label="Numer seryjny")
    password = forms.CharField(max_length=100, required=False, label="Hasło zabezpieczające")
    visual_status = forms.CharField(
        label="Stan wizualny",
        required=False,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40})
    )
    todo = forms.CharField(
        required=False,
        label="Do zrobienia",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40})
    )
    additional_info = forms.CharField(
        required=False,
        label="Dodatkowe informacje",
        widget=forms.Textarea(attrs={"rows": 4, "cols": 40})
    )
    priority = forms.ChoiceField(
        choices=(
            ("low", "Niski"),
            ("medium", "Średni"),
            ("high", "Wysoki"),
        ),
        required=False,
        label="Priorytet"
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        required=False,
        label="Wybierz istniejącego klienta bądź podaj dane poniżej aby utworzyć nowego"
    )
    customer_email = forms.EmailField(required=False, label="Email")
    customer_phone = forms.CharField(max_length=20, required=False, label="Numer telefonu")
    customer_name = forms.CharField(max_length=100, required=False, label="Imię i nazwisko")

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')
        customer_email = cleaned_data.get('customer_email')
        customer_phone = cleaned_data.get('customer_phone')
        customer_name = cleaned_data.get('customer_name')

        if not customer and not (customer_email and customer_phone and customer_name):
            raise forms.ValidationError("You must select a customer or provide customer details.")

        return cleaned_data

    class Meta:
        model = RepairItem
        fields = ['serial_number', 'password', 'visual_status', 'todo', 'additional_info', 'priority', 'customer']