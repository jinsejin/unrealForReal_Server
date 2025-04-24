from django.contrib import admin
from .models import Located, Asset, MaintenanceReport, RepairHistory, SensorData


@admin.register(Located)
class LocatedAdmin(admin.ModelAdmin):
    list_display = ('campus_name', 'building_name', 'room_name', 'coordinates')
    search_fields = ('campus_name', 'building_name', 'room_name')
    list_filter = ('campus_name', 'building_name')


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'state', 'building_name', 'room_name', 'install_date')
    search_fields = ('name', 'asset_id')
    list_filter = ('category', 'state', 'room__building_name')
    autocomplete_fields = ['room']
    readonly_fields = ['building_name', 'room_name']


@admin.register(MaintenanceReport)
class MaintenanceReportAdmin(admin.ModelAdmin):
    list_display = ('asset', 'user', 'priority', 'failure_type', 'is_resolved', 'reported_at', 'building_name')
    search_fields = ('user', 'description', 'asset__name')
    list_filter = ('priority', 'failure_type', 'is_resolved', 'reported_at')
    autocomplete_fields = ['asset']
    readonly_fields = ['building_name']


@admin.register(RepairHistory)
class RepairHistoryAdmin(admin.ModelAdmin):
    list_display = ('report', 'repaired_by', 'repaired_at')
    search_fields = ('repaired_by', 'report__asset__name')
    readonly_fields = ('repaired_at',)
    autocomplete_fields = ['report']


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'humidity', 'angle', 'is_door_open')
    list_filter = ('is_door_open', 'timestamp')
    readonly_fields = ('timestamp',)
