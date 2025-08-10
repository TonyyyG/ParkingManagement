import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_management.settings')
django.setup()

from parking.models import ParkingLot

# 获取所有停车场
lots = ParkingLot.objects.all()

print('修复前的可用车位数量:')
print('停车场名称 | 总车位 | 数据库可用车位 | 实际可用车位')
print('-' * 50)

# 先显示修复前的状态
for lot in lots:
    actual_available = lot.spaces.filter(status='available').count()
    print(f'{lot.name} | {lot.total_spaces} | {lot.available_spaces} | {actual_available}')

print('-' * 50)
print('开始修复...')

# 修复每个停车场的可用车位数量
fixed_count = 0
for lot in lots:
    actual_available = lot.spaces.filter(status='available').count()
    if lot.available_spaces != actual_available:
        lot.available_spaces = actual_available
        lot.save()
        print(f'✅ 已修复: {lot.name} 的可用车位数量从 {lot.available_spaces} 更新为 {actual_available}')
        fixed_count += 1
    else:
        print(f'✅ 无需修复: {lot.name} 的可用车位数量已正确')

print('-' * 50)
print(f'修复完成。共修复了 {fixed_count} 个停车场的可用车位数量。')