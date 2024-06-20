import uuid
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
import io
from reportlab.pdfbase.ttfonts import TTFont
from typing import List, Any, Optional
from workshop.models import RepairItem, Estimate
from reportlab.platypus import SimpleDocTemplate, Table, Image, Paragraph, Spacer


def add_spaces(elements, height=7):
    elements.append(Spacer(1, height))


def add_text(elements: List, style, text: str) -> None:
    elements.append(Paragraph(text, style))


def get_paragraph_style() -> Any:
    paragraph_style = ParagraphStyle('services_description')
    paragraph_style.fontName = 'Abhaya'
    paragraph_style.fontSize = 8
    paragraph_style.bold = False
    return paragraph_style


def get_header_style() -> Any:
    header_style = ParagraphStyle('header')
    header_style.fontName = 'Abhaya'
    header_style.fontSize = 10
    header_style.bold = True
    return header_style


def generate_filename(start: str, repair_item: Optional[RepairItem] = None, estimate: Optional[Estimate] = None) -> str:
    if repair_item:
        return f"{start}_{repair_item.id}_{repair_item.created_at}.pdf"
    if estimate:
        return f"{start}_{estimate.id}_{estimate.created_at}.pdf"
    else:
        return f"{start}_{uuid.uuid4()}.pdf"


def generate_estimate(estimate: Estimate):
    # Define your styles
    style = get_paragraph_style()
    header_style = get_header_style()

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Abhaya", "Abhaya.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    header_text = f"WYCENA: {estimate.name}"

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 2 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 2 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29 02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
    )

    data = [
        [logo, address_paragraph],
        ["Imię i nazwisko zleceniodawcy", f"{estimate.customer.name}"],
        ["Data", f"{str(estimate.created_at)[:11]}"],
        ["Telefon kontaktowy:", f"{estimate.customer.phone}"],
        ["Adres email:", f"{estimate.customer.email}"],
    ]
    estimate_data = [["Nazwa", "Kwota"], ]

    estimate_costs = estimate.costs.all()
    for cost in estimate_costs:
        estimate_data.append([cost.name, f"{cost.amount} zł"])
    estimate_data.append(["Kwota całkowita", f"{sum(c.amount for c in estimate_costs)} zł"])

    # Define column widths for consistency
    col_widths = [3 * inch, 3 * inch]

    table = Table(data, colWidths=col_widths)
    estimate_table = Table(estimate_data, colWidths=col_widths)

    table_style = [
        ('FONT', (0, 0), (-1, -1), 'Abhaya', 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]
    table.setStyle(table_style)
    estimate_table.setStyle(table_style)

    # Add elements to the PDF
    elements.append(Paragraph(header_text, header_style))
    elements.append(Paragraph("<br/><br/>", style))  # add spaces
    elements.append(table)
    elements.append(Paragraph("<br/><br/>", style))  # add spaces
    elements.append(estimate_table)
    elements.append(Paragraph("<br/><br/>", style))  # add spaces

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="wycena", estimate=estimate)

    return buffer, filename

def generate_acceptance_protocol(repair_item: RepairItem):
    style = get_paragraph_style()
    header_style = get_header_style()

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Abhaya", "Abhaya.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    header_text = "PROTOKÓŁ PRZYJĘCIA SPRZĘTU DO SERWISU"
    services_description = f"Usługi serwisowe (naprawa, konfiguracja, diagnoza/sprawdzenie, czyszczenie). Dokładny opis wykonanych rzeczy:"
    signature_left = "Podpis Zleceniodawcy"
    signature_right = "Data i podpis osoby odbierającej sprzęt"

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 2 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 2 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29 02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
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
        ('FONT', (0, 0), (-1, -1), 'Abhaya', 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table.setStyle(table_style)

    add_text(elements, header_style, header_text)
    add_spaces(elements)
    elements.append(table)
    add_spaces(elements)
    add_text(elements, style, services_description)
    add_spaces(elements)
    add_text(elements, style, f"{repair_item.done if repair_item.done else '...'}")
    add_spaces(elements)

    signature_data = [
        [signature_left, signature_right]
    ]

    signature_table = Table(signature_data, colWidths=[3 * inch, 3 * inch])
    signature_table_style = [
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Abhaya', 10),
    ]

    signature_table.setStyle(signature_table_style)
    elements.append(signature_table)

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="wydanie", repair_item=repair_item)

    return buffer, filename


def generate_admission_protocol(repair_item):
    style = get_paragraph_style()
    header_style = get_header_style()

    buffer = io.BytesIO()
    pdfmetrics.registerFont(TTFont("Abhaya", "Abhaya.ttf"))
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    visual_text = "Stan wizualny:"
    header_text = "PROTOKÓŁ PRZYJĘCIA SPRZĘTU DO SERWISU"
    services_description = "Usługi serwisowe (naprawa, konfiguracja, diagnoza/sprawdzenie, czyszczenie). Dokładny opis usterki:"
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
    signature_left = "Podpis Zleceniodawcy"
    signature_right = "Data i podpis osoby odbierającej sprzęt"

    statutes = [statute_description_1, statute_description_2, statute_description_3, statute_description_4,
                statute_description_5, statute_description_6, statute_description_7, statute_description_8,
                statute_description_9]

    logo_path = 'logo.png'
    logo = Image(logo_path)
    logo.drawHeight = 2 * inch * logo.drawHeight / logo.drawWidth
    logo.drawWidth = 2 * inch
    address_paragraph = Paragraph(
        "Adres: Tadeusza Kościuszki 29 02-495 Warszawa<br/>Telefon Serwisu: 509-621-580", style
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
        ('FONT', (0, 0), (-1, -1), 'Abhaya', 8),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
    ]

    table.setStyle(table_style)

    add_text(elements, header_style, header_text)
    add_spaces(elements)
    elements.append(table)
    add_spaces(elements)
    add_text(elements, style, visual_text)
    add_spaces(elements)
    add_text(elements, style, f"{repair_item.visual_status if repair_item.visual_status else '...'}")
    add_spaces(elements)

    add_text(elements, style, services_description)
    add_spaces(elements)
    add_text(elements, style, f"{repair_item.todo if repair_item.todo else '...'}")
    add_spaces(elements)

    for statute in statutes:
        add_text(elements, style, statute)
    add_spaces(elements)
    add_text(elements, style, statute_end)
    add_spaces(elements)

    signature_data = [
        [signature_left, signature_right]
    ]

    signature_table = Table(signature_data, colWidths=[3 * inch, 3 * inch])
    signature_table_style = [
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Abhaya', 10),
    ]

    signature_table.setStyle(signature_table_style)
    elements.append(signature_table)

    doc.build(elements)

    buffer.seek(0)

    filename = generate_filename(start="przyjecie", repair_item=repair_item)

    return buffer, filename
