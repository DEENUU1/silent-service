from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from workshop.models import Customer, RepairItem, Estimate, Costs, Notes


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


class SearchEstimateForm(forms.Form):
    search_query = forms.CharField(
        label="Szukaj",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Znajdź wycenę"}),
    )


class RepairItemStatusForm(forms.Form):
    status = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].label = "Zlecenie zakończone"


class RepairItemPriorityForm(forms.Form):
    PRIORITY = (
        ("", "------"),
        ("low", "Niski"),
        ("medium", "Średni"),
        ("high", "Wysoki"),
    )

    priority = forms.ChoiceField(choices=PRIORITY, required=False, label="Priorytet")


class EstimateCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Nazwa")
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

        if not customer and not (customer_phone and customer_name):
            raise forms.ValidationError("You must select a customer or provide customer details.")

        return cleaned_data

    class Meta:
        model = Estimate
        fields = ['customer', 'name']


class RepairItemCreateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Nazwa")
    serial_number = forms.CharField(max_length=100, required=False, label="Numer seryjny")
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

        if not customer and not (customer_phone and customer_name):
            raise forms.ValidationError("You must select a customer or provide customer details.")

        return cleaned_data

    class Meta:
        model = RepairItem
        fields = ['name', 'serial_number', 'password', 'visual_status', 'todo', 'additional_info', 'priority', 'customer']


class EstimateCostsForm(forms.ModelForm):
    class Meta:
        model = Costs
        fields = ['name', 'cost_type', 'amount', 'estimate']
        widgets = {
            'estimate': forms.HiddenInput()
        }


class RepairItemCostsForm(forms.ModelForm):
    class Meta:
        model = Costs
        fields = ['name', 'cost_type', 'amount', 'repair_item']
        widgets = {
            'repair_item': forms.HiddenInput()
        }


class EstimateIdForm(forms.Form):
    estimate_id = forms.IntegerField(label='Estimate ID')


class RepairItemUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = RepairItem
        labels = {
            'status': '',
        }
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=[(False, "Do zrobienia"), (True, "Zrobione")])
        }


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['multiple'] = True


class NotesForm(forms.ModelForm):
    listing_images = MultipleFileField(required=False, label='Files')

    class Meta:
        model = Notes
        fields = ['name', 'text']
        labels = {
            'name': 'Tytuł',
            'text': 'Treść'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


class CustomerCreateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ("name", "email", "phone")
        labels = {
            "name": "Imie i nazwisko",
            "email": "Email",
            "phone": "Numer telefonu",
        }


class RepairItemUpdateForm(forms.ModelForm):
    class Meta:
        model = RepairItem
        fields = ['name', 'serial_number', 'status', 'done', 'password', 'visual_status', 'todo', 'additional_info', 'priority', 'customer']
        labels = {
            'name': 'Nazwa',
            'serial_number': 'Numer seryjny',
            'password': 'Hasło zabezpieczające',
            'visual_status': 'Stan wizualny',
            'todo': 'Do zrobienia',
            'additional_info': 'Dodatkowe informacje',
            'done': 'Zrobione',
            'status': 'Zakończone',
            'priority': 'Priorytet',
            'customer': 'Klient',
        }


class EstimateUpdateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['name', 'customer']
        labels = {
            'name': 'Nazwa',
            'customer': 'Klient',
        }


class NotesUpdateForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['name', 'text']
        labels = {
            'name': 'Tytuł',
            'text': 'Treść'
        }


class CostsUpdateForm(forms.ModelForm):
    class Meta:
        model = Costs
        fields = ['name', 'cost_type', 'amount']
        labels = {
            'name': 'Nazwa',
            'cost_type': 'Typ',
            'amount': 'Kwota',
        }
