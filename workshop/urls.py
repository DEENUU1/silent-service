from django.urls import path
from workshop.views import (
    CustomerListView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
    CustomerDetailView,
    RepairItemListView,
    RepairItemCreateView,
    RepairItemDeleteView,
    RepairItemDetailView,
    RepairItemUpdateView,
    CostsCreateView,
    CostsUpdateView,
    CostsDeleteView,
    AdmissionProtocolView,
)

app_name = "workshop"


urlpatterns = [
    path('admission_protocol/<int:pk>/', AdmissionProtocolView.as_view(), name='admission-protocol'),

    path('customer/', CustomerListView.as_view(), name="customer-list"),
    path('customer/create/', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name="customer-delete"),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name="customer-detail"),

    path('', RepairItemListView.as_view(), name="repair-item-list"),
    path('create/', RepairItemCreateView.as_view(), name="repair-item-create"),
    path('<int:pk>/delete/', RepairItemDeleteView.as_view(), name="repair-item-delete"),
    path('<int:pk>/', RepairItemDetailView.as_view(), name="repair-item-detail"),
    path('<int:pk>/update/', RepairItemUpdateView.as_view(), name="repair-item-update"),

    path('costs/create/', CostsCreateView.as_view(), name="costs-create"),
    path('costs/<int:pk>/delete/', CostsDeleteView.as_view(), name="costs-delete"),
    path('costs/<int:pk>/update/', CostsUpdateView.as_view(), name="costs-update"),
]
