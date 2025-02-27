from django.contrib import admin
from .models import Campus, Building, Floor, Room, Asset, MaintenanceReport, RepairHistory

# Campus (캠퍼스)
@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 리스트에 보이는 필드
    search_fields = ('name',)  # 검색 필드 추가


# Building (건물)
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'campus')
    list_filter = ('campus',)
    search_fields = ('name', 'campus__name')


# Floor (층)
@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'building')
    list_filter = ('building',)
    search_fields = ('number', 'building__name')


# Room (방/공간)
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'floor', 'building_name')
    list_filter = ('floor__building',)
    search_fields = ('name', 'floor__number', 'floor__building__name')

    def building_name(self, obj):
        return obj.floor.building.name  # 건물 이름을 가져오기
    building_name.admin_order_field = 'floor__building__name'
    building_name.short_description = '건물 이름'


# Asset (사물/설비)
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'room', 'floor_name', 'building_name', 'state')
    list_filter = ('category', 'state', 'room__floor__building')
    search_fields = ('name', 'category', 'room__name', 'room__floor__building__name')

    def floor_name(self, obj):
        return obj.room.floor.number  # 층 번호 가져오기
    floor_name.admin_order_field = 'room__floor__number'
    floor_name.short_description = '층 번호'

    def building_name(self, obj):
        return obj.room.floor.building.name  # 건물 이름 가져오기
    building_name.admin_order_field = 'room__floor__building__name'
    building_name.short_description = '건물 이름'


# Maintenance Report (고장 신고)
@admin.register(MaintenanceReport)
class MaintenanceReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset', 'user', 'priority', 'is_resolved', 'reported_at')
    list_filter = ('priority', 'is_resolved', 'asset__room__floor__building')
    search_fields = ('asset__name', 'user', 'priority', 'asset__room__floor__building__name')


# Repair History (수리 이력)
@admin.register(RepairHistory)
class RepairHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'report', 'repaired_by', 'repaired_at')
    list_filter = ('repaired_by',)
    search_fields = ('report__asset__name', 'repaired_by')
