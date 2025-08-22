from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """购物车项内联编辑"""
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """购物车管理界面配置"""
    list_display = ['id', 'user', 'session_id', 'created_at', 'updated_at', 'get_total_price']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['id', 'user__username', 'session_id']
    inlines = [CartItemInline]  # 内联显示购物车项
    date_hierarchy = 'created_at'
    ordering = ['-updated_at']
    readonly_fields = ['created_at', 'updated_at', 'get_total_price']  # 只读字段

    # 在列表页显示购物车总价
    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = '购物车总价'
