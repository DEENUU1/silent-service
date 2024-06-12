from django.contrib import admin
from workshop.models import RepairItem, Costs, Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    list_filter = ('name',)
    search_fields = ('name',)


class RepairItemAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'priority', 'status', 'customer')
    list_filter = ('priority', 'status')
    search_fields = ('serial_number',)
    list_editable = ('priority', 'status')


class CostsAdmin(admin.ModelAdmin):
    list_display = ('cost_type', 'amount')
    list_filter = ('cost_type',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(RepairItem, RepairItemAdmin)
admin.site.register(Costs, CostsAdmin)
