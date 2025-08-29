from django.urls import path
from . import views

app_name = 'accounts'  # 命名空间

urlpatterns = [
    path('register/', views.register, name='register'),  # 注册页面
    path('profile/', views.profile, name='profile'), # 使用自定义登录# 个人资料页面
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # 新增
    path('password-change/', views.password_change, name='password_change'),  # 新增
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorite/toggle/<int:product_id>/', views.favorite_toggle, name='favorite_toggle'),
    path('merchant/apply/', views.merchant_apply, name='merchant_apply'),# 新增商户申请路由
]
