import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_management.settings')
django.setup()

from django.contrib.auth.models import User

# 检查是否已存在超级用户
if not User.objects.filter(username='admin').exists():
    # 创建超级用户
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print('超级用户已创建：用户名=admin，密码=admin123')
else:
    print('超级用户已存在')