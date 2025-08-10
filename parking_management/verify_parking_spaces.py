import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_management.settings')
django.setup()

from parking.models import ParkingLot

# 获取所有停车场
lots = ParkingLot.objects.all()

print('停车场名称 | 总车位 | 数据库可用车位 | 实际可用车位')
print('-' * 50)

# 遍历每个停车场并比较可用车位数量
for lot in lots:
    actual_available = lot.spaces.filter(status='available').count()
    print(f'{lot.name} | {lot.total_spaces} | {lot.available_spaces} | {actual_available}')
    if lot.available_spaces != actual_available:
        print(f'⚠️ 不一致: {lot.name} 的可用车位数量需要更新!')

print('-' * 50)
print('验证完成。')