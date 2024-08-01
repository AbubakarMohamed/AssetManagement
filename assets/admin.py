from django.contrib import admin
from .models import Asset, Lend, Maintenance

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_quantity', 'available_quantity', 'unique_id', 'arrival_date')
    search_fields = ('name', 'unique_id')
    list_filter = ('arrival_date',)

@admin.register(Lend)
class LendAdmin(admin.ModelAdmin):
    list_display = ('asset', 'quantity', 'lent_date', 'returned_date', 'condition', 'quantity_good', 'quantity_bad')
    search_fields = ('asset__name', 'condition')
    list_filter = ('lent_date', 'returned_date', 'condition')

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('asset', 'quantity', 'maintenance_date', 'is_fixed')
    search_fields = ('asset__name',)
    list_filter = ('maintenance_date', 'is_fixed')
