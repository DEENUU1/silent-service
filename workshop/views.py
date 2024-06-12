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
from workshop.forms import SearchForm


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
        return reverse_lazy("workshop:customer-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Klient został dodany")
        return queryset


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ["name", "phone", "email"]
    template_name = "workshop/customer_update.html"

    def get_success_url(self):
        return reverse_lazy("workshop:customer-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Klient został zaaktualizowany")
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

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["repair_items"] = RepairItem.objects.filter(customer=self.object)
        return context
