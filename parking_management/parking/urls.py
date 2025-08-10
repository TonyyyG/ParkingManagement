from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    
    # 停车位相关URL
    path('spaces/', views.parking_space_list, name='parking_space_list'),
    path('spaces/<int:pk>/', views.parking_space_detail, name='parking_space_detail'),
    path('spaces/create/', views.parking_space_create, name='parking_space_create'),
    path('spaces/<int:pk>/update/', views.parking_space_update, name='parking_space_update'),
    path('spaces/<int:pk>/delete/', views.parking_space_delete, name='parking_space_delete'),
    
    # 停车场相关URL
    path('lots/', views.parking_lot_list, name='parking_lot_list'),
    path('lots/<int:pk>/', views.parking_lot_detail, name='parking_lot_detail'),
    path('lots/create/', views.parking_lot_create, name='parking_lot_create'),
    path('lots/<int:pk>/update/', views.parking_lot_update, name='parking_lot_update'),
    path('lots/<int:pk>/delete/', views.parking_lot_delete, name='parking_lot_delete'),
    
    # 车辆相关URL
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/create/', views.vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    
    # 停车记录相关URL
    path('records/', views.parking_record_list, name='parking_record_list'),
    path('records/<int:pk>/', views.parking_record_detail, name='parking_record_detail'),
    path('records/create/', views.parking_record_create, name='parking_record_create'),
    path('records/<int:pk>/update/', views.parking_record_update, name='parking_record_update'),
    path('records/<int:pk>/delete/', views.parking_record_delete, name='parking_record_delete'),
]