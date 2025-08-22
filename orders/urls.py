from django.urls import path
from . import views

app_name = 'orders'  # 命名空间

urlpatterns = [
    path('create/', views.order_create, name='order_create'),  # 创建订单
    path('', views.order_list, name='order_list'),  # 订单列表
    path('<int:order_id>/', views.order_detail, name='order_detail'),  # 订单详情
]
