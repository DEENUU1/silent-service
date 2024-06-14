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
from workshop.models import Customer, RepairItem, Costs
from workshop.forms import (
    SearchForm,
    RepairItemPriorityForm,
    RepairItemStatusForm,
)
from workshop.services.costs import calculate_total_costs_by_repair_item


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
                name__icontains=search_query
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
        context["q"] = SearchForm(self.request.GET)
        context["status_form"] = RepairItemStatusForm()
        context["priority_form"] = RepairItemPriorityForm()
        return context


class RepairItemCreateView(LoginRequiredMixin, CreateView):
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
    template_name = "workshop/repair_item_create.html"
    
    def get_success_url(self):
        messages.success(self.request, "Urządzenie zostało dodane")
        return reverse_lazy("workshop:repair-item-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


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


class RepairItemDetailView(LoginRequiredMixin, DetailView):
    model = RepairItem
    template_name = "workshop/repair_item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["costs"] = Costs.objects.filter(repair_item=self.object)
        context["total_costs"] = calculate_total_costs_by_repair_item(self.object)
        return context


class CostsCreateView(LoginRequiredMixin, CreateView):
    model = Costs
    fields = ["amount", "cost_type", "repair_item"]
    template_name = "workshop/costs_create.html"

    def get_success_url(self):
        messages.success(self.request, "Koszt został dodany")
        return reverse_lazy("workshop:repair-item-detail", kwargs={"pk": self.object.repair_item.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


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
