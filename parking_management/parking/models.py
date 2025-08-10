from django.db import models
from django.utils import timezone

class ParkingLot(models.Model):
    """停车场模型"""
    name = models.CharField(max_length=100, verbose_name="停车场名称")
    address = models.CharField(max_length=200, verbose_name="停车场地址")
    description = models.TextField(blank=True, null=True, verbose_name="停车场描述")
    total_spaces = models.IntegerField(verbose_name="总车位数")
    available_spaces = models.IntegerField(default=0, verbose_name="可用车位数")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "停车场"
        verbose_name_plural = "停车场管理"

class ParkingSpace(models.Model):
    """停车位模型"""
    STATUS_CHOICES = (
        ('available', '可用'),
        ('occupied', '已占用'),
        ('reserved', '已预约'),
        ('maintenance', '维护中'),
    )
    
    number = models.CharField(max_length=10, verbose_name="车位编号")
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name="spaces", verbose_name="所属停车场")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="状态")
    is_handicapped = models.BooleanField(default=False, verbose_name="残疾人车位")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return f"{self.parking_lot.name} - {self.number}"
    
    class Meta:
        verbose_name = "停车位"
        verbose_name_plural = "停车位管理"

class Vehicle(models.Model):
    """车辆模型"""
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="车牌号")
    vehicle_type = models.CharField(max_length=50, verbose_name="车辆类型")
    owner_name = models.CharField(max_length=100, verbose_name="车主姓名")
    owner_phone = models.CharField(max_length=20, verbose_name="车主电话")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return self.license_plate
    
    class Meta:
        verbose_name = "车辆"
        verbose_name_plural = "车辆管理"

class ParkingRecord(models.Model):
    """停车记录模型"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="parking_records", verbose_name="车辆")
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, related_name="parking_records", verbose_name="停车位")
    start_time = models.DateTimeField(default=timezone.now, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="费用")
    is_paid = models.BooleanField(default=False, verbose_name="是否已支付")
    vehicle_photo = models.ImageField(upload_to='vehicle_photos/', null=True, blank=True, verbose_name="车辆照片")
    
    def __str__(self):
        return f"{self.vehicle.license_plate} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        verbose_name = "停车记录"
        verbose_name_plural = "停车记录管理"
