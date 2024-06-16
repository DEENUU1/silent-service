from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from workshop.models import Customer, RepairItem, Costs, Estimate
from workshop.forms import (
    SearchForm,
    RepairItemPriorityForm,
    RepairItemStatusForm,
    SearchRepairItemForm,
    RepairItemCreateForm,
    EstimateCreateForm,
    SearchEstimateForm, EstimateCostsForm, RepairItemCostsForm
)
from workshop.services.costs import calculate_total_costs_by_repair_item, calculate_total_costs_by_estimate
from workshop.services.repair_item_stats import get_repair_item_statistics
from django.http import FileResponse
from workshop.services.protocol import generate_admission_protocol, generate_acceptance_protocol
from django.views import View


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

        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = SearchRepairItemForm(self.request.GET)
        context["status_form"] = RepairItemStatusForm()
        context["priority_form"] = RepairItemPriorityForm()
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

    context = {
        'object': repair_item,
        'costs': costs,
        'total_costs': calculate_total_costs_by_repair_item(costs),
        'form': form
    }

    return render(request, 'workshop/repair_item_detail.html', context)


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


