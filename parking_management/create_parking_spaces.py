import os
import django
import random

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_management.settings')
django.setup()

from parking.models import ParkingLot, ParkingSpace

# 获取所有停车场
lots = ParkingLot.objects.all()

print('开始添加停车位数据...')

for lot in lots:
    print(f'处理停车场: {lot.name} (总车位: {lot.total_spaces})')
    
    # 计算已有的停车位数量
    existing_spaces = ParkingSpace.objects.filter(parking_lot=lot).count()
    
    # 计算还能添加的停车位数量
    available_slots = lot.total_spaces - existing_spaces
    
    if available_slots <= 0:
        print(f'⚠️ {lot.name} 已达到最大车位数，无需添加。')
        continue
    
    print(f'将为 {lot.name} 添加 {available_slots} 个停车位...')
    
    # 添加停车位
    added_count = 0
    for i in range(1, lot.total_spaces + 1):
        # 检查该编号的停车位是否已存在
        if not ParkingSpace.objects.filter(parking_lot=lot, number=i).exists():
            # 随机决定是否为残疾人车位 (10% 的概率)
            is_handicapped = random.random() < 0.1
            
            # 创建停车位
            ParkingSpace.objects.create(
                parking_lot=lot,
                number=i,
                status='available',  # 默认设置为可用
                is_handicapped=is_handicapped
            )
            
            added_count += 1
            
            # 如果已添加足够的停车位，退出循环
            if added_count >= available_slots:
                break
    
    print(f'✅ 成功为 {lot.name} 添加了 {added_count} 个停车位。')
    
    # 更新停车场的可用车位数量
    lot.available_spaces = lot.spaces.filter(status='available').count()
    lot.save()

print('-' * 50)
print('停车位数据添加完成。')