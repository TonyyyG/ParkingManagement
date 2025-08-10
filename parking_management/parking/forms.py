from django import forms
from .models import ParkingSpace, ParkingRecord, Vehicle, ParkingLot

class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ['number', 'parking_lot', 'status', 'is_handicapped']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'parking_lot': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_handicapped': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ParkingRecordForm(forms.ModelForm):
    class Meta:
        model = ParkingRecord
        fields = ['vehicle', 'parking_space', 'start_time', 'end_time', 'fee', 'is_paid', 'vehicle_photo']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'parking_space': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vehicle_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ParkingRecordUpdateForm(forms.ModelForm):
    class Meta:
        model = ParkingRecord
        fields = ['end_time', 'fee', 'is_paid', 'vehicle_photo']
        widgets = {
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vehicle_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class ParkingRecordPhotoForm(forms.ModelForm):
    """专门用于上传停车记录车辆照片的表单"""
    class Meta:
        model = ParkingRecord
        fields = ['vehicle_photo']
        widgets = {
            'vehicle_photo': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'owner_name', 'owner_phone']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control'}),
            'owner_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ParkingLotForm(forms.ModelForm):
    class Meta:
        model = ParkingLot
        fields = ['name', 'address', 'description', 'total_spaces', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'total_spaces': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }