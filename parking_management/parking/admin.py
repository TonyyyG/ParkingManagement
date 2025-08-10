from django.contrib import admin
from .models import ParkingLot, ParkingSpace, Vehicle, ParkingRecord

@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'total_spaces', 'available_spaces', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    list_filter = ('created_at', 'updated_at')

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('number', 'parking_lot', 'status', 'is_handicapped', 'created_at', 'updated_at')
    search_fields = ('number', 'parking_lot__name')
    list_filter = ('status', 'is_handicapped', 'parking_lot')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'vehicle_type', 'owner_name', 'owner_phone', 'created_at', 'updated_at')
    search_fields = ('license_plate', 'owner_name')
    list_filter = ('vehicle_type', 'created_at')

@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'parking_space', 'start_time', 'end_time', 'fee', 'is_paid')
    search_fields = ('vehicle__license_plate', 'parking_space__number')
    list_filter = ('is_paid', 'start_time')
