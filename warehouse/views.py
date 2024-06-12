from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from warehouse.models import Device
from warehouse.forms import (
    SearchForm,
    DeviceTypeForm
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


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


class CreateDeviceView(LoginRequiredMixin, CreateView):
    model = Device
    template_name = "warehouse/device_create.html"
    fields = ("name", "quantity", "device_type")

    def get_success_url(self):
        return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Przedmiot został dodany")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = "warehouse/device_detail.html"


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = "warehouse/device_update.html"
    fields = ("name", "quantity", "device_type")

    def get_success_url(self):
        return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Przedmiot został zaktualizowany")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteDeviceView(LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy("warehouse:device-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Przedmiot został usunięty")
        return queryset
