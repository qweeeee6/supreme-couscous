from django.urls import path
from . import views

app_name = 'accounts'  # 命名空间

urlpatterns = [
    path('register/', views.register, name='register'),  # 注册页面
    path('profile/', views.profile, name='profile'),     # 个人资料页面
]
