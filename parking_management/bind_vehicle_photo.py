import os
import django
from pathlib import Path

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_management.settings')
django.setup()

from parking.models import Vehicle, ParkingRecord
from django.core.files import File

# 配置信息
TARGET_LICENSE_PLATE = '粤A123456'
PHOTO_PATH = 'c:\\Users\\56888\\Desktop\\ParkMag_WebProject\\038CC.png'

# 主函数
def main():
    try:
        # 查找目标车辆(粤A123456)
        try:
            target_vehicle = Vehicle.objects.get(license_plate=TARGET_LICENSE_PLATE)
            print(f'找到目标车辆: {target_vehicle.license_plate}')
        except Vehicle.DoesNotExist:
            print(f'错误: 未找到车牌号为 {TARGET_LICENSE_PLATE} 的车辆')
            return

        # 检查图片文件是否存在
        if not os.path.exists(PHOTO_PATH):
            print(f'错误: 图片文件不存在: {PHOTO_PATH}')
            return

        # 处理图片
        with open(PHOTO_PATH, 'rb') as f:
            # 为目标车辆创建停车记录并添加图片
            # 查找目标车辆的所有停车记录
            all_records = ParkingRecord.objects.filter(vehicle=target_vehicle)
            if all_records:
                # 更新所有记录
                updated_count = 0
                for record in all_records:
                    record.vehicle_photo.save(os.path.basename(PHOTO_PATH), File(f))
                    updated_count += 1
                    print(f'已更新停车记录 {record.id} 的车辆照片')
                print(f'共更新 {updated_count} 条停车记录')
            else:
                # 创建新记录
                print('目标车辆没有停车记录，正在创建新记录...')
                # 查找一个可用的停车位
                from parking.models import ParkingSpace
                available_space = ParkingSpace.objects.filter(status='available').first()
                if available_space:
                    new_record = ParkingRecord.objects.create(
                        vehicle=target_vehicle,
                        parking_space=available_space,
                        start_time=django.utils.timezone.now()
                    )
                    new_record.vehicle_photo.save(os.path.basename(PHOTO_PATH), File(f))
                    print(f'已创建新停车记录 {new_record.id} 并添加车辆照片')
                    # 更新停车位状态
                    available_space.status = 'occupied'
                    available_space.save()
                else:
                    print('错误: 没有可用的停车位，无法创建新停车记录')

        print('任务完成!')

    except Exception as e:
        print(f'发生错误: {str(e)}')

if __name__ == '__main__':
    main()