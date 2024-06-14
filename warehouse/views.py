from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from reportlab.pdfbase.ttfonts import TTFont

from warehouse.models import Device
from warehouse.forms import (
    SearchForm,
    DeviceTypeForm
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import FileResponse
import io


def some_view(request):
    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))

    # Utworzenie obiektu dokumentu PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    # Styl dla nagłówka
    styles = getSampleStyleSheet()
    # Dodanie nagłówka do dokumentu
    header_text = "PROTOKÓŁ PRZYJĘCIA SPRZĘTU DO SERWISU"
    header_style = ParagraphStyle('header')
    header_style.fontName = 'Verdana'
    elements.append(Paragraph(header_text, header_style))

    # Definicja danych do tabeli
    data = [
        ["Logo graficzne", "Adres", "Telefon Serwisu:"],
        ["xxxxxxxxxxxx", "", ""],
        ["Imię i nazwisko zleceniodawcy", "", ""],
        ["Data przyjęcia", "", ""],
        ["Telefon kontaktowy:", "", ""],
        ["Adres email:", "", ""],
        ["Nazwa sprzętu:", "", ""],
        ["Numery seryjne:", "", ""],
        ["Stan wizualny:", "", ""],
        ["Hasło zabezpieczające:", "", ""]
    ]

    # Tworzenie tabeli
    table = Table(data)
    table_style = [
        ('FONT', (0, 0), (-1, -1), 'Verdana', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table.setStyle(table_style)
    elements.append(table)
    elements.append(Paragraph("<br/><br/>", header_style))  # Dodatkowa pusta linia

    # Dodanie długiego opisu usług serwisowych za pomocą paragrafu
    services_description = "Usługi serwisowe (naprawa, konfiguracja, diagnoza/sprawdzenie, czyszczenie). " \
                           "Dokładny opis usterki: <br/><br/>" \
                           "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed dui ligula, placerat a " \
                           "lacus nec, dignissim dapibus leo. Ut accumsan turpis turpis, nec placerat purus " \
                           "condimentum a. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices " \
                           "posuere cubilia curae; Quisque varius augue erat, ut volutpat sem lobortis id. " \
                           "Ut vitae quam nec risus convallis porta. Ut egestas mi lectus, sed pharetra diam " \
                           "viverra et. Sed fermentum commodo lorem, eget euismod mi suscipit vel. Nullam " \
                           "feugiat, arcu ac porttitor consectetur, magna augue elementum dui, at imperdiet " \
                           "enim lectus pellentesque mi. Duis lacinia massa vel nulla consequat, at vestibulum " \
                           "turpis euismod. Nulla facilisi. Integer eu condimentum eros. Nunc eu sapien vitae " \
                           "magna auctor faucibus. Donec cursus lacinia diam, ac commodo quam. Nam in laoreet " \
                           "sem. Interdum et malesuada fames ac ante ipsum primis in faucibus. Lorem ipsum dolor " \
                           "sit amet, consectetur adipiscing elit."

    services_description_style = ParagraphStyle('services_description')
    services_description_style.fontName = 'Verdana'
    elements.append(Paragraph(services_description, services_description_style))
    elements.append(Paragraph("<br/><br/>", header_style))
    elements.append(Paragraph("<br/><br/>", header_style))

    statute_description = """1.Klient zobowiązany jest do umieszczenia w Zleceniu prawdziwych danych osobowych oraz wskazania danych umożliwiających nawiązanie z nim kontaktu przez Serwis.
2.Serwis, w sytuacjach określonych w niniejszym Regulaminie, będzie nawiązywał kontakt z Klientem za pomocą: telefonicznie i/lub pocztą elektroniczną , w zależności od danych wskazanych przez Klienta w Zleceniu.
3.Klient ma prawo do odstąpienia od umowy serwisowej w przypadku, gdy nie zaakceptuje kosztów związanych z naprawą urządzenia. W celu odstąpienia od umowy serwisowej Klient zobowiązany jest złożyć, stosowne oświadczenie na piśmie do siedziby Serwisu.
4.W przypadku akceptacji przez klienta kosztów naprawy, oszacowanie usterki jest bezpłatne . Jeżeli Klient rezygnuje z usług serwisowych i tym samym odstępuje od umowy serwisowej, zostanie obciążony opłatą za oględziny. Minimalna opłata za oględziny równa jest cenie 1 roboczogodziny pracy Serwisu.
5.Serwis nie ponosi odpowiedzialności za wady ukryte przekazanego do naprawy sprzętu oraz nieprawidłowości w jego funkcjonowaniu, o ile uszkodzenia te nie dotyczą w sposób bezpośredni usterki, której naprawa została Serwisowi zlecona.
6.Klient zobowiązany jest do odbioru sprzętu z Serwisu w terminie maksymalnie 14 dni od daty powiadomienia przez serwis o gotowości urządzenia do odbioru . Po upływie 14 dni od skutecznego poinformowania Klienta o możliwości odbioru sprzętu przyjmuje się, że Klient oddał sprzęt w przechowanie w rozumieniu art. 835 Kodeksu Cywilnego. W takim przypadku, klient może zostać obciążony opłatą magazynową w wysokości 10 zł (brutto) za każdy rozpoczęty dzień przechowania sprzętu. Opłata magazynowa pobierana jest również po upływie 14 dni od daty 
7.Serwis udziela 90 dniowej gwarancji na naprawę jednak tylko w zakresie usuniętej usterki. W przypadku reklamacji Klient powinien złożyć ją w formie pisemnej. Serwis zobowiązany jest ustosunkować się do reklamacji złożonej przez Klienta w terminie do 14 dni od jej otrzymania.
8.W przypadku nie odebrania powierzonego sprzętu przez klienta w ciągu 3 miesięcy od daty powiadomienia o możliwości odbioru sprzętu. Powierzone urządzenie uważa się za porzucone w rozumieniu art. 180 kodeksu cywilnego. W tym wypadku zostaje zezłomowane lub sprzedane na wolnym rynku, w celu zwrotu poniesionych kosztów przez serwis. wypowiedzenia umowy lub odstąpienia od umowy przez Klienta, jeżeli w tym czasie nie odebrał on sprzętu od Serwisu. Opłata magazynowa jest doliczana do ceny usług serwisowej oraz płatna przed wydaniem sprzętu Klientowi.
9.Oddając sprzęt do naprawy Klient dobrowolnie akceptuje niniejszy Regulamin, a jego postanowienia są wiążące dla Klienta i Serwisu chyba, że inne postanowienia zostaną przedstawione i zaakceptowane przez obie strony w formie pisemnej."""

    statute_description_style = ParagraphStyle('statute_description')
    statute_description_style.fontName = 'Verdana'
    elements.append(Paragraph(statute_description, statute_description_style))

    elements.append(Paragraph("<br/><br/>", header_style))


    # Zapisanie wszystkich elementów do dokumentu PDF
    doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="protokol_przyjecia.pdf")



class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = "warehouse/device_list.html"
    paginate_by = 50
    ordering = "name"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        device_type = self.request.GET.get("device_type")
        if device_type:
            queryset = queryset.filter(device_type__name=device_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = SearchForm(self.request.GET)
        context["device_types"] = DeviceTypeForm(self.request.GET)
        return context


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    template_name = "warehouse/device_create.html"
    fields = ("name", "quantity", "device_type")

    def get_success_url(self):
        messages.success(self.request, "Przedmiot został dodany")
        return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = "warehouse/device_detail.html"


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = "warehouse/device_update.html"
    fields = ("name", "quantity", "device_type")

    def get_success_url(self):
        messages.success(self.request, "Przedmiot został zaktualizowany")
        return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy("warehouse:device-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Przedmiot został usunięty")
        return queryset
