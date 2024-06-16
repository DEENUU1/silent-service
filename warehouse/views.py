from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from warehouse.models import Device, DeviceType
from warehouse.forms import (
    SearchForm,
    DeviceTypeForm,
    DeviceTypeSearchForm
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


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    template_name = "warehouse/device_create.html"
    fields = ("name", "quantity", "device_type")

    def get_success_url(self):
        messages.success(self.request, "Przedmiot został dodany")
        # return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})
        return reverse_lazy("warehouse:device-list")

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
        # return reverse_lazy("warehouse:device-detail", kwargs={"pk": self.object.pk})
        return reverse_lazy("warehouse:device-list")

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


class DeviceTypeListView(LoginRequiredMixin, ListView):
    model = DeviceType
    template_name = "warehouse/device_type_list.html"
    paginate_by = 50
    ordering = "name"

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("search_query")
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = DeviceTypeSearchForm(self.request.GET)
        return context


class DeviceTypeCreateView(LoginRequiredMixin, CreateView):
    model = DeviceType
    template_name = "warehouse/device_type_create.html"
    fields = ("name",)

    def get_success_url(self):
        messages.success(self.request, "Kategoria została dodana")
        return reverse_lazy("warehouse:device-type-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class DeviceTypeDetailView(LoginRequiredMixin, DetailView):
    model = DeviceType
    template_name = "warehouse/device_type_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["devices"] = Device.objects.filter(device_type=self.object)
        context["device_count"] = context["devices"].count()
        return context


class DeviceTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = DeviceType
    template_name = "warehouse/device_type_update.html"
    fields = ("name",)

    def get_success_url(self):
        messages.success(self.request, "Kategoria została zaaktualizowana")
        return reverse_lazy("warehouse:device-type-detail", kwargs={"pk": self.object.pk})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class DeviceTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = DeviceType
    success_url = reverse_lazy("warehouse:device-type-list")

    def get_queryset(self):
        queryset = super().get_queryset()
        messages.success(self.request, "Kategoria została usunięta")
        return queryset
