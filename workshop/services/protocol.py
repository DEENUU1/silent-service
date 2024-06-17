import uuid
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
import io
from reportlab.pdfbase.ttfonts import TTFont
from typing import List, Any, Optional
from workshop.models import RepairItem, Estimate
from reportlab.platypus import SimpleDocTemplate, Table, Image, Paragraph

def add_spaces(elements: List, style) -> None:
    elements.append(Paragraph("<br/><br/>", style))


def add_text(elements: List, style, text: str) -> None:
    elements.append(Paragraph(text, style))


def get_paragraph_style() -> Any:
    paragraph_style = ParagraphStyle('services_description')
    paragraph_style.fontName = 'Verdana'
    return paragraph_style


def generate_filename(start: str, repair_item: Optional[RepairItem] = None, estimate: Optional[Estimate] = None) -> str:
    if repair_item:
        return f"{start}_{repair_item.id}_{repair_item.created_at}.pdf"
    if estimate:
        return f"{start}_{estimate.id}_{estimate.created_at}.pdf"
    else:
        return f"{start}_{uuid.uuid4()}.pdf"


def generate_estimate(estimate: Estimate):
    style = get_paragraph_style()
    header_style = ParagraphStyle('header')

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    header_text = f"WYCENA: {estimate.name}"

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 0.5 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 0.5 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29<br/>02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
    )

    data = [
        [logo, address_paragraph],
        ["Imię i nazwisko zleceniodawcy", f"{estimate.customer.name}"],
        ["Data", f"{str(estimate.created_at)[:11]}"],
        ["Telefon kontaktowy:", f"{estimate.customer.phone}"],
        ["Adres email:", f"{estimate.customer.email}"],
        ["", ""],
        ["Nazwa", "Kwota"]
    ]

    estimate_costs = estimate.costs.all()
    for cost in estimate_costs:
        data.append([cost.name, f"{cost.amount} zł"])
    data.append(["Kwota całkowita", f"{sum(c.amount for c in estimate_costs)}"])

    table = Table(data)
    table_style = [
        ('FONT', (0, 0), (-1, -1), 'Verdana', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]
    table.setStyle(table_style)

    add_text(elements, style, header_text)
    add_spaces(elements, header_style)
    elements.append(table)
    add_spaces(elements, header_style)

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="wycena", estimate=estimate)

    return buffer, filename


def generate_acceptance_protocol(repair_item: RepairItem):
    style = get_paragraph_style()
    header_style = ParagraphStyle('header')

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    header_text = "PROTOKÓŁ PRZYJĘCIA SPRZĘTU DO SERWISU"
    services_description = f"Usługi serwisowe (naprawa, konfiguracja, diagnoza/sprawdzenie, czyszczenie). Dokładny opis wykonanych rzeczy:"
    signature = "Podpis Zleceniodawcy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data i podpis osoby odbierającej sprzęt: "

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 0.5 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 0.5 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29<br/>02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
    )

    data = [
        [logo, address_paragraph],
        ["Imię i nazwisko zleceniodawcy", f"{repair_item.customer.name}"],
        ["Data przyjęcia", f"{str(repair_item.created_at)[:11]}"],
        ["Telefon kontaktowy:", f"{repair_item.customer.phone}"],
        ["Adres email:", f"{repair_item.customer.email}"],
        ["Nazwa sprzętu:", ""],
        ["Numery seryjne:", f"{repair_item.serial_number}"],
        ["Hasło zabezpieczające:", f"{repair_item.password}"],
    ]

    table = Table(data)
    table_style = [
        ('FONT', (0, 0), (-1, -1), 'Verdana', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table.setStyle(table_style)

    add_text(elements, style, header_text)
    add_spaces(elements, header_style)
    elements.append(table)
    add_spaces(elements, header_style)
    add_text(elements, style, services_description)
    add_spaces(elements, header_style)
    add_text(elements, style, f"{repair_item.done}")
    add_spaces(elements, header_style)
    add_text(elements, style, signature)

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="wydanie", repair_item=repair_item)

    return buffer, filename


def generate_admission_protocol(repair_item: RepairItem):
    style = get_paragraph_style()
    header_style = ParagraphStyle('header')

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Verdana", "Verdana.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    visual_text = "Stan wizualny:"
    header_text = "PROTOKÓŁ PRZYJĘCIA SPRZĘTU DO SERWISU"
    services_description = f"Usługi serwisowe (naprawa, konfiguracja, diagnoza/sprawdzenie, czyszczenie). Dokładny opis usterki:"
    statute_description_1 = "1.Klient zobowiązany jest do umieszczenia w Zleceniu prawdziwych danych osobowych oraz wskazania danych umożliwiających nawiązanie z nim kontaktu przez Serwis"
    statute_description_2 = "2.Serwis, w sytuacjach określonych w niniejszym Regulaminie, będzie nawiązywał kontakt z Klientem za pomocą: telefonicznie i/lub pocztą elektroniczną , w zależności od danych wskazanych przez Klienta w Zleceniu."
    statute_description_3 = "3.Klient ma prawo do odstąpienia od umowy serwisowej w przypadku, gdy nie zaakceptuje kosztów związanych z naprawą urządzenia. W celu odstąpienia od umowy serwisowej Klient zobowiązany jest złożyć, stosowne oświadczenie na piśmie do siedziby Serwisu."
    statute_description_4 = "4.W przypadku akceptacji przez klienta kosztów naprawy, oszacowanie usterki jest bezpłatne . Jeżeli Klient rezygnuje z usług serwisowych i tym samym odstępuje od umowy serwisowej, zostanie obciążony opłatą za oględziny. Minimalna opłata za oględziny równa jest cenie 1 roboczogodziny pracy Serwisu."
    statute_description_5 = "5.Serwis nie ponosi odpowiedzialności za wady ukryte przekazanego do naprawy sprzętu oraz nieprawidłowości w jego funkcjonowaniu, o ile uszkodzenia te nie dotyczą w sposób bezpośredni usterki, której naprawa została Serwisowi zlecona."
    statute_description_6 = "6.Klient zobowiązany jest do odbioru sprzętu z Serwisu w terminie maksymalnie 14 dni od daty powiadomienia przez serwis o gotowości urządzenia do odbioru . Po upływie 14 dni od skutecznego poinformowania Klienta o możliwości odbioru sprzętu przyjmuje się, że Klient oddał sprzęt w przechowanie w rozumieniu art. 835 Kodeksu Cywilnego. W takim przypadku, klient może zostać obciążony opłatą magazynową w wysokości 10 zł (brutto) za każdy rozpoczęty dzień przechowania sprzętu. Opłata magazynowa pobierana jest również po upływie 14 dni od daty "
    statute_description_7 = "7.Serwis udziela 90 dniowej gwarancji na naprawę jednak tylko w zakresie usuniętej usterki. W przypadku reklamacji Klient powinien złożyć ją w formie pisemnej. Serwis zobowiązany jest ustosunkować się do reklamacji złożonej przez Klienta w terminie do 14 dni od jej otrzymania."
    statute_description_8 = "8.W przypadku nie odebrania powierzonego sprzętu przez klienta w ciągu 3 miesięcy od daty powiadomienia o możliwości odbioru sprzętu. Powierzone urządzenie uważa się za porzucone w rozumieniu art. 180 kodeksu cywilnego. W tym wypadku zostaje zezłomowane lub sprzedane na wolnym rynku, w celu zwrotu poniesionych kosztów przez serwis. wypowiedzenia umowy lub odstąpienia od umowy przez Klienta, jeżeli w tym czasie nie odebrał on sprzętu od Serwisu. Opłata magazynowa jest doliczana do ceny usług serwisowej oraz płatna przed wydaniem sprzętu Klientowi."
    statute_description_9 = "9.Oddając sprzęt do naprawy Klient dobrowolnie akceptuje niniejszy Regulamin, a jego postanowienia są wiążące dla Klienta i Serwisu chyba, że inne postanowienia zostaną przedstawione i zaakceptowane przez obie strony w formie pisemnej."
    statute_end = "Niniejszy Protokół jest dokumentem uprawniającym do odbioru sprzętu."
    signature = "Podpis Zleceniodawcy&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Data i podpis osoby odbierającej sprzęt: "
    statutes = [statute_description_1, statute_description_2, statute_description_3, statute_description_4,
                statute_description_5, statute_description_6, statute_description_7, statute_description_8,
                statute_description_9]

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 0.5 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 0.5 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29<br/>02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
    )

    data = [
        [logo, address_paragraph],
        ["Imię i nazwisko zleceniodawcy", f"{repair_item.customer.name}"],
        ["Data przyjęcia", f"{str(repair_item.created_at)[:11]}"],
        ["Telefon kontaktowy:", f"{repair_item.customer.phone}"],
        ["Adres email:", f"{repair_item.customer.email}"],
        ["Nazwa sprzętu:", ""],
        ["Numery seryjne:", f"{repair_item.serial_number}"],
        ["Hasło zabezpieczające:", f"{repair_item.password}"],
    ]

    table = Table(data)
    table_style = [
        ('FONT', (0, 0), (-1, -1), 'Verdana', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table.setStyle(table_style)

    add_text(elements, style, header_text)
    add_spaces(elements, header_style)
    elements.append(table)
    add_spaces(elements, header_style)
    add_text(elements, style, visual_text)
    add_spaces(elements, header_style)
    add_text(elements, style, f"{repair_item.visual_status}")
    add_spaces(elements, header_style)

    add_text(elements, style, services_description)
    add_spaces(elements, header_style)
    add_text(elements, style, repair_item.todo)
    add_spaces(elements, header_style)

    for statute in statutes:
        add_text(elements, style, statute)
    add_spaces(elements, header_style)
    add_text(elements, style, statute_end)
    add_spaces(elements, header_style)
    add_text(elements, style, signature)

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="przyjecie", repair_item=repair_item)

    return buffer, filename
