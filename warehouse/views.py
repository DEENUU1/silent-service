from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from warehouse.models import Device, DeviceType
from warehouse.forms import SearchForm


class DeviceListView(ListView):
    model = Device
    template_name = "warehouse/device_list.html"
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
        context["q"] = SearchForm(self.request.GET)
        return context
