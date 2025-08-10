from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import ParkingLot, ParkingSpace, Vehicle, ParkingRecord
from .forms import ParkingSpaceForm, ParkingRecordForm, VehicleForm, ParkingLotForm, ParkingRecordUpdateForm

# 停车位视图

def parking_space_list(request):
    spaces = ParkingSpace.objects.all()
    return render(request, 'parking/spaces/list.html', {'spaces': spaces})

def parking_space_detail(request, pk):
    space = get_object_or_404(ParkingSpace, pk=pk)
    return render(request, 'parking/spaces/detail.html', {'space': space})

def parking_space_create(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '停车位创建成功！')
            return redirect('parking_space_list')
    else:
        form = ParkingSpaceForm()
    return render(request, 'parking/spaces/create.html', {'form': form})

def parking_space_update(request, pk):
    space = get_object_or_404(ParkingSpace, pk=pk)
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST, instance=space)
        if form.is_valid():
            form.save()
            messages.success(request, '停车位更新成功！')
            return redirect('parking_space_detail', pk=space.pk)
    else:
        form = ParkingSpaceForm(instance=space)
    return render(request, 'parking/spaces/update.html', {'form': form, 'parking_space': space})

def parking_space_delete(request, pk):
    space = get_object_or_404(ParkingSpace, pk=pk)
    if request.method == 'POST':
        space.delete()
        messages.success(request, '停车位删除成功！')
        return redirect('parking_space_list')
    return render(request, 'parking/spaces/detail.html', {'parking_space': space})

# 停车场视图

def parking_lot_list(request):
    lots = ParkingLot.objects.all()
    # 动态计算每个停车场的可用车位数量并更新数据库
    for lot in lots:
        available_spaces = lot.spaces.filter(status='available').count()
        if lot.available_spaces != available_spaces:
            lot.available_spaces = available_spaces
            lot.save()
    return render(request, 'parking/lots/list.html', {'parking_lots': lots})

def parking_lot_detail(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    parking_spaces = ParkingSpace.objects.filter(parking_lot=lot)
    # 动态计算可用车位数量
    available_spaces = parking_spaces.filter(status='available').count()
    used_spaces = lot.total_spaces - available_spaces
    occupancy_rate = (used_spaces / lot.total_spaces) * 100 if lot.total_spaces > 0 else 0
    # 设置可用车位属性，但不保存到数据库
    lot.available_spaces = available_spaces
    return render(request, 'parking/lots/detail.html', {
        'parking_lot': lot,
        'parking_spaces': parking_spaces,
        'used_spaces': used_spaces,
        'occupancy_rate': occupancy_rate
    })

def parking_lot_create(request):
    if request.method == 'POST':
        form = ParkingLotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '停车场创建成功！')
            return redirect('parking_lot_list')
    else:
        form = ParkingLotForm()
    return render(request, 'parking/lots/create.html', {'form': form})

def parking_lot_update(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    if request.method == 'POST':
        form = ParkingLotForm(request.POST, instance=lot)
        if form.is_valid():
            form.save()
            messages.success(request, '停车场更新成功！')
            return redirect('parking_lot_detail', pk=lot.pk)
    else:
        form = ParkingLotForm(instance=lot)
    return render(request, 'parking/lots/update.html', {'form': form, 'parking_lot': lot})

def parking_lot_delete(request, pk):
    lot = get_object_or_404(ParkingLot, pk=pk)
    if request.method == 'POST':
        lot.delete()
        messages.success(request, '停车场删除成功！')
        return redirect('parking_lot_list')
    return render(request, 'parking/lots/confirm_delete.html', {'parking_lot': lot})

# 车辆视图

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'parking/vehicles/list.html', {'vehicles': vehicles})

def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    parking_records = ParkingRecord.objects.filter(vehicle=vehicle).order_by('-start_time')
    return render(request, 'parking/vehicles/detail.html', {'vehicle': vehicle, 'parking_records': parking_records})

def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '车辆创建成功！')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'parking/vehicles/create.html', {'form': form})

def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, '车辆更新成功！')
            return redirect('vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'parking/vehicles/update.html', {'form': form, 'vehicle': vehicle})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, '车辆删除成功！')
        return redirect('vehicle_list')
    return render(request, 'parking/vehicles/confirm_delete.html', {'vehicle': vehicle})

# 首页视图

def home(request):
    # 统计信息
    total_lots = ParkingLot.objects.count()
    total_spaces = ParkingSpace.objects.count()
    available_spaces = ParkingSpace.objects.filter(status='available').count()
    total_vehicles = Vehicle.objects.count()
    total_records = ParkingRecord.objects.count()
    
    context = {
        'total_lots': total_lots,
        'total_spaces': total_spaces,
        'available_spaces': available_spaces,
        'total_vehicles': total_vehicles,
        'total_records': total_records,
    }
    return render(request, 'parking/home.html', context)

# 停车记录视图

def parking_record_list(request):
    # 确保获取最新的停车记录数据
    records = ParkingRecord.objects.all().order_by('-start_time')
    return render(request, 'parking/records/list.html', {'records': records})

def parking_record_create(request):
    if request.method == 'POST':
        form = ParkingRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            # 更新停车位状态为已占用
            parking_space = record.parking_space
            parking_space.status = 'occupied'
            parking_space.save()
            # 更新停车场可用车位
            parking_lot = parking_space.parking_lot
            parking_lot.available_spaces -= 1
            parking_lot.save()
            record.save()
            messages.success(request, '停车记录创建成功！')
            return redirect('parking_record_list')
    else:
        form = ParkingRecordForm()
    return render(request, 'parking/records/create.html', {'form': form})

import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def parking_record_update(request, pk):
    record = get_object_or_404(ParkingRecord, pk=pk)
    logger.debug(f'更新停车记录: {record.id}, 当前结束时间: {record.end_time}')
    
    if request.method == 'POST':
        form = ParkingRecordUpdateForm(request.POST, request.FILES, instance=record)
        logger.debug(f'表单验证状态: {form.is_valid()}')
        
        if not form.is_valid():
            logger.debug(f'表单数据: {request.POST}')
            logger.debug(f'表单错误: {form.errors}')
        
        if form.is_valid():
            logger.debug(f'表单数据: {form.cleaned_data}')
            
            # 如果结束时间不为空，更新停车位状态和停车场可用车位
            cleaned_data = form.cleaned_data
            end_time = cleaned_data['end_time']
            fee = cleaned_data['fee']
            is_paid = cleaned_data['is_paid']

            # 如果结束时间不为空且之前为空，更新停车位状态和停车场可用车位
            if end_time and not record.end_time:
                # 计算停车时长（小时）
                duration = (end_time - record.start_time).total_seconds() / 3600
                
                # 如果费用未设置，按每小时10元计算
                if not fee:
                    fee = round(duration * 10, 2)
                    form.instance.fee = fee

                # 更新停车位状态
                parking_space = record.parking_space
                parking_space.status = 'available'
                parking_space.save()

                # 更新停车场可用车位
                parking_lot = parking_space.parking_lot
                parking_lot.available_spaces += 1
                parking_lot.save()

            # 保存表单数据
            record = form.save()
            logger.debug(f'停车记录更新成功: {record.id}, 新的结束时间: {record.end_time}')
            messages.success(request, '停车记录更新成功！')
            
            # 确保重定向到列表页面时获取最新数据
            return redirect('parking_record_list')
    else:
        form = ParkingRecordForm(instance=record)
    
    return render(request, 'parking/records/update.html', {'form': form, 'parking_record': record})

def parking_record_detail(request, pk):
    record = get_object_or_404(ParkingRecord, pk=pk)
    # 计算停车时长（小时）
    duration = None
    if record.end_time:
        duration = (record.end_time - record.start_time).total_seconds() / 3600
    return render(request, 'parking/records/detail.html', {
        'parking_record': record,
        'duration': duration
    })

def parking_record_delete(request, pk):
    record = get_object_or_404(ParkingRecord, pk=pk)
    if request.method == 'POST':
        # 如果记录尚未完成，恢复停车位状态和停车场可用车位
        if not record.end_time:
            parking_space = record.parking_space
            parking_space.status = 'available'
            parking_space.save()
            parking_lot = parking_space.parking_lot
            parking_lot.available_spaces += 1
            parking_lot.save()
        record.delete()
        messages.success(request, '停车记录删除成功！')
        return redirect('parking_record_list')
    return render(request, 'parking/records/confirm_delete.html', {'parking_record': record})
