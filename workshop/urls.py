from django.urls import path
from workshop.views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    CustomerDetailView,
)

app_name = "workshop"


urlpatterns = [
    path('customer/', CustomerListView.as_view(), name="customer-list"),
    path('customer/create/', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name="customer-delete"),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name="customer-detail"),
]
