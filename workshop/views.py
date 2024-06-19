from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from workshop.models import Customer, RepairItem, Costs, Estimate, Notes, Files
from workshop.forms import (
    SearchForm,
    RepairItemPriorityForm,
    RepairItemStatusForm,
    SearchRepairItemForm,
    RepairItemCreateForm,
    EstimateCreateForm,
    SearchEstimateForm,
    EstimateCostsForm,
    RepairItemCostsForm,
    RepairItemUpdateStatusForm, NotesForm
)
from workshop.services.costs import calculate_total_costs_by_repair_item, calculate_total_costs_by_estimate
from workshop.services.filename_generator import generate_filename_timestamp
from workshop.services.repair_item_stats import get_repair_item_statistics
from django.http import FileResponse, JsonResponse
from workshop.services.protocol import generate_admission_protocol, generate_acceptance_protocol, generate_estimate
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When
from django.db import models


class AdmissionProtocolView(LoginRequiredMixin, View):
    def get(self, request, pk: int):
        obj = RepairItem.objects.get(pk=pk)
        file, filename = generate_admission_protocol(obj)
        return FileResponse(file, as_attachment=True, filename=filename)


class AcceptanceProtocolView(LoginRequiredMixin, View):
    def get(self, request, pk: int):
        obj = RepairItem.objects.get(pk=pk)
        file, filename = generate_acceptance_protocol(obj)
        return FileResponse(file, as_attachment=True, filename=filename)


class EstimateProtocolView(LoginRequiredMixin, View):
    def get(self, request, pk: int):
        obj = Estimate.objects.get(pk=pk)
        file, filename = generate_estimate(obj)
        return FileResponse(file, as_attachment=True, filename=filename)


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = "workshop/customer_list.html"
    paginate_by = 50
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = SearchForm(self.request.GET)
        return context


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    fields = ["name", "phone", "email"]
    template_name = "workshop/customer_create.html"

    def get_success_url(self):
        messages.success(self.request, "Klient został dodany")
        return reverse_lazy("workshop:customer-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ["name", "phone", "email"]
    template_name = "workshop/customer_update.html"

    def get_success_url(self):
        messages.success(self.request, "Klient został zaaktualizowany")
        return reverse_lazy("workshop:customer-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy("workshop:customer-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Klient został usunięty")
        return queryset


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = "workshop/customer_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repair_items"] = RepairItem.objects.filter(customer=self.object)
        context["estimates"] = Estimate.objects.filter(customer=self.object)
        context["notes"] = Notes.objects.filter(customer=self.object)
        return context


class RepairItemListView(LoginRequiredMixin, ListView):
    model = RepairItem
    template_name = "workshop/repair_item_list.html"
    paginate_by = 50
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(
                serial_number__icontains=search_query
            )

        status = self.request.GET.get("status")
        if status == "on":
            queryset = queryset.filter(status=True)
        if status is None:
            queryset = queryset.filter(status=False)

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        now = timezone.now()

        three_days_ago = now - timedelta(days=3)

        queryset = queryset.annotate(
            priority_order=Case(
                When(priority='high', then=1),
                When(priority='medium', then=2),
                When(priority='low', then=3),
                default=4,
                output_field=models.IntegerField(),
            ),
            recent_created_at=Case(
                When(created_at__gt=three_days_ago, then=1),
                default=0,
                output_field=models.IntegerField(),
            )
        )

        queryset = queryset.order_by(
            'priority_order',
            '-recent_created_at',
            '-created_at'
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = SearchRepairItemForm(self.request.GET)
        context["status_form"] = RepairItemStatusForm(self.request.GET)
        context["priority_form"] = RepairItemPriorityForm(self.request.GET)
        context["stats"] = get_repair_item_statistics()
        return context


class RepairItemCreateView(LoginRequiredMixin, CreateView):
    model = RepairItem
    form_class = RepairItemCreateForm
    template_name = "workshop/repair_item_create.html"

    def get_success_url(self):
        messages.success(self.request, "Urządzenie zostało dodane")
        return reverse_lazy("workshop:repair-item-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def form_valid(self, form):
        customer = form.cleaned_data.get('customer')
        if not customer:
            customer_email = form.cleaned_data.get('customer_email')
            customer_phone = form.cleaned_data.get('customer_phone')
            customer_name = form.cleaned_data.get('customer_name')

            existing_customer = Customer.objects.filter(email=customer_email).first()

            if existing_customer:
                customer = existing_customer
            else:
                customer = Customer.objects.create(
                    email=customer_email,
                    phone=customer_phone,
                    name=customer_name
                )

        repair_item = form.save(commit=False)
        repair_item.customer = customer
        repair_item.save()

        return super().form_valid(form)


class RepairItemUpdateView(LoginRequiredMixin, UpdateView):
    model = RepairItem
    fields = [
        "serial_number",
        "password",
        "visual_status",
        "todo",
        "additional_info",
        "done",
        "status",
        "priority",
        "customer"
    ]
    template_name = "workshop/repair_item_update.html"

    def get_success_url(self):
        messages.success(self.request, "Urządzenie zostało zaaktualizowane")
        return reverse_lazy("workshop:repair-item-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class RepairItemDeleteView(LoginRequiredMixin, DeleteView):
    model = RepairItem
    success_url = reverse_lazy("workshop:repair-item-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Urządzenie zostało usunięte")
        return queryset


def repair_item_detail(request, pk: int):
    repair_item = get_object_or_404(RepairItem, id=pk)

    if request.method == 'POST':
        form = RepairItemCostsForm(request.POST)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.repair_item = repair_item
            cost.save()
            return redirect('workshop:repair-item-detail', pk=pk)
    else:
        form = RepairItemCostsForm(initial={'object': repair_item})

    costs = repair_item.costs.all()
    status_form = RepairItemUpdateStatusForm(instance=repair_item)
    notes = Notes.objects.filter(repair_item=repair_item)

    context = {
        'object': repair_item,
        'costs': costs,
        'total_costs': calculate_total_costs_by_repair_item(costs),
        'form': form,
        'status_form': status_form,
        'notes': notes,
    }

    return render(request, 'workshop/repair_item_detail.html', context)


@require_GET
def autocomplete_costs(request):
    term = request.GET.get('term', '')
    costs = Costs.objects.filter(name__icontains=term)[:10]
    results = []
    for cost in costs:
        results.append({
            'id': cost.id,
            'name': cost.name,
            'amount': str(cost.amount),
            'cost_type': cost.cost_type,
        })
    return JsonResponse(results, safe=False)


def repair_item_update_status(request, pk):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        repair_item = get_object_or_404(RepairItem, pk=pk)
        form = RepairItemUpdateStatusForm(request.POST, instance=repair_item)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'ok', 'new_status': repair_item.status})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'invalid request'}, status=400)


class CostsUpdateView(LoginRequiredMixin, UpdateView):
    model = Costs
    fields = ["amount", "cost_type", "repair_item"]
    template_name = "workshop/costs_update.html"

    def get_success_url(self):
        messages.success(self.request, "Koszt został zaaktualizowany")
        return reverse_lazy("workshop:repair-item-detail", kwargs={"pk": self.object.repair_item.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class CostsDeleteView(LoginRequiredMixin, DeleteView):
    model = Costs
    success_url = reverse_lazy("workshop:repair-item-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Koszt został usunięty")
        return queryset


class EstimateListView(LoginRequiredMixin, ListView):
    model = Estimate
    template_name = "workshop/estimate_list.html"
    paginate_by = 50
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = SearchEstimateForm(self.request.GET)
        return context


def estimate_detail(request, pk: int):
    estimate = get_object_or_404(Estimate, id=pk)

    if request.method == 'POST':
        form = EstimateCostsForm(request.POST)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.estimate = estimate
            cost.save()
            return redirect('workshop:estimate-detail', pk=pk)
    else:
        form = EstimateCostsForm(initial={'estimate': estimate})

    costs = estimate.costs.all()

    context = {
        'estimate': estimate,
        'costs': costs,
        'total_costs': calculate_total_costs_by_estimate(costs),
        'form': form
    }

    return render(request, 'workshop/estimate_detail.html', context)


class EstimateCreateView(LoginRequiredMixin, CreateView):
    model = Estimate
    form_class = EstimateCreateForm
    template_name = "workshop/estimate_create.html"

    def get_success_url(self):
        messages.success(self.request, "Wycena została utworzona")
        return reverse_lazy("workshop:estimate-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def form_valid(self, form):
        customer = form.cleaned_data.get('customer')
        if not customer:
            customer_email = form.cleaned_data.get('customer_email')
            customer_phone = form.cleaned_data.get('customer_phone')
            customer_name = form.cleaned_data.get('customer_name')

            existing_customer = Customer.objects.filter(email=customer_email).first()

            if existing_customer:
                customer = existing_customer
            else:
                customer = Customer.objects.create(
                    email=customer_email,
                    phone=customer_phone,
                    name=customer_name
                )

        repair_item = form.save(commit=False)
        repair_item.customer = customer
        repair_item.save()

        return super().form_valid(form)


class EstimateUpdateView(LoginRequiredMixin, UpdateView):
    model = Estimate
    fields = [
        "name",
        "customer",
    ]
    template_name = "workshop/estimate_update.html"

    def get_success_url(self):
        messages.success(self.request, "Wycena została zaaktualizowana")
        return reverse_lazy("workshop:estimate-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class EstimateDeleteView(LoginRequiredMixin, DeleteView):
    model = Estimate
    success_url = reverse_lazy("workshop:estimate-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Wycena została usunięta")
        return queryset


def convert_estimate_to_repair_item(request, pk):
    estimate = get_object_or_404(Estimate, id=pk)

    if estimate.converted:
        messages.error(request, "Wycena jest już przekonwertowana")
        return redirect('workshop:repair-item-detail', pk=estimate.repair_item.pk)

    repair_item = RepairItem.objects.create(
        serial_number=estimate.name,
        customer=estimate.customer,
    )

    costs = estimate.costs.all()
    for cost in costs:
        Costs.objects.create(
            name=cost.name,
            amount=cost.amount,
            cost_type=cost.cost_type,
            repair_item=repair_item
        )
    estimate.converted = True
    estimate.repair_item = repair_item
    estimate.save()
    messages.success(request, "Zlecenie zostało utworzone")
    return redirect('workshop:repair-item-detail', pk=repair_item.pk)


class CreateNotesPerRepairItemView(View):
    def get(self, request, pk: int):
        repairitem = get_object_or_404(RepairItem, id=pk)
        form = NotesForm()
        context = {
            'form': form,
            'repairitem': repairitem,
        }
        return render(request, 'workshop/notes_create.html', context)

    def post(self, request, pk: int):
        repairitem = get_object_or_404(RepairItem, id=pk)
        form = NotesForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']

            note = Notes.objects.create(
                name=name,
                text=text,
                repair_item=repairitem,
                customer=repairitem.customer
            )

            files = request.FILES.getlist('listing_images')
            for file in files:
                file_instance = Files.objects.create(file=generate_filename_timestamp(file))
                note.files.add(file_instance)

            return redirect('workshop:repair-item-detail',  pk=repairitem.pk)

        context = {
            'form': form,
            'repairitem': repairitem,
        }
        return render(request, 'workshop/notes_create.html', context)


class CreateNotesPerCustomerItemView(View):
    def get(self, request, pk: int):
        customer = get_object_or_404(Customer, id=pk)
        form = NotesForm()
        context = {
            'form': form,
            'customer': customer,
        }
        return render(request, 'workshop/notes_create.html', context)

    def post(self, request, pk: int):
        customer = get_object_or_404(Customer, id=pk)
        form = NotesForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']

            note = Notes.objects.create(
                name=name,
                text=text,
                customer=customer
            )

            files = request.FILES.getlist('listing_images')
            for file in files:
                file_instance = Files.objects.create(file=generate_filename_timestamp(file))
                note.files.add(file_instance)

            return redirect('workshop:estimate-list')

        context = {
            'form': form,
            'customer': customer,
        }
        return render(request, 'workshop/notes_create.html', context)


class NotesUpdateView(LoginRequiredMixin, UpdateView):
    model = Notes
    fields = ["name", "text"]
    template_name = "workshop/notes_update.html"

    def get_success_url(self):
        messages.success(self.request, "Notatka została zaaktualizowana")
        return reverse_lazy("workshop:notes-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class NotesDetailView(LoginRequiredMixin, DetailView):
    model = Notes
    template_name = "workshop/notes_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["files"] = self.object.files.all()
        return context


class NotesDeleteView(LoginRequiredMixin, DeleteView):
    model = Notes
    success_url = reverse_lazy("workshop:repair-item-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Notatka została usunięta")
        return queryset


class FileCreateByNotesView(View):
    def post(self, request, pk: int):
        note = get_object_or_404(Notes, id=pk)
        files = request.FILES.getlist('listing_images')
        for file in files:
            file_instance = Files.objects.create(file=generate_filename_timestamp(file))
            note.files.add(file_instance)
        return redirect('workshop:notes-detail', pk=note.pk)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = Files
    success_url = reverse_lazy("workshop:customer-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Plik został usunięty")
        return queryset
