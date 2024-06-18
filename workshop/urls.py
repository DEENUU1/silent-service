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
    repair_item_detail,
    RepairItemUpdateView,
    CostsUpdateView,
    CostsDeleteView,
    AdmissionProtocolView,
    AcceptanceProtocolView,
    EstimateCreateView,
    EstimateUpdateView,
    EstimateDeleteView,
    estimate_detail,
    EstimateListView,
    convert_estimate_to_repair_item,
    EstimateProtocolView,
    repair_item_update_status
)

app_name = "workshop"


urlpatterns = [
    path('estimate/', EstimateListView.as_view(), name='estimate-list'),
    path('estimate/create/', EstimateCreateView.as_view(), name='estimate-create'),
    path('estimate/<int:pk>/delete/', EstimateDeleteView.as_view(), name='estimate-delete'),
    path('estimate/<int:pk>/update/', EstimateUpdateView.as_view(), name='estimate-update'),
    path('estimate/<int:pk>/', estimate_detail, name='estimate-detail'),
    path('estimate/<int:pk>/convert/', convert_estimate_to_repair_item, name='estimate-convert'),
    path('estimate_protocol/<int:pk>/', EstimateProtocolView.as_view(), name='estimate-protocol'),

    path('admission_protocol/<int:pk>/', AdmissionProtocolView.as_view(), name='admission-protocol'),
    path('acceptance_protocol/<int:pk>/', AcceptanceProtocolView.as_view(), name='acceptance-protocol'),

    path('customer/', CustomerListView.as_view(), name="customer-list"),
    path('customer/create/', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name="customer-delete"),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name="customer-detail"),

    path('', RepairItemListView.as_view(), name="repair-item-list"),
    path('create/', RepairItemCreateView.as_view(), name="repair-item-create"),
    path('<int:pk>/delete/', RepairItemDeleteView.as_view(), name="repair-item-delete"),
    path('<int:pk>/', repair_item_detail, name="repair-item-detail"),
    path('<int:pk>/update/', RepairItemUpdateView.as_view(), name="repair-item-update"),
    path('<int:pk>/update_status/',  repair_item_update_status, name="repair-item-update-status"),

    path('costs/<int:pk>/delete/', CostsDeleteView.as_view(), name="costs-delete"),
    path('costs/<int:pk>/update/', CostsUpdateView.as_view(), name="costs-update"),
]
