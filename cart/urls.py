from django.urls import path
from . import views

app_name = 'cart'  # 命名空间，必须添加

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # 购物车详情页
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),  # 添加商品
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),  # 移除商品
]
