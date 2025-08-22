from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """订单项内联编辑"""
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0  # 不显示额外的空表单


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """订单管理界面配置"""
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'phone',
                    'status', 'total_price', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['id', 'user__username', 'first_name', 'last_name', 'email']
    inlines = [OrderItemInline]  # 内联显示订单项
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']  # 只读字段
