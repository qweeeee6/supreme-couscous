from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # 自动从名称生成slug


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'updated_at']
    list_editable = ['price', 'available']  # 可在列表页直接编辑的字段
    prepopulated_fields = {'slug': ('name',)}  # 自动从名称生成slug
    search_fields = ['name', 'description']  # 搜索字段
    date_hierarchy = 'created_at'  # 按日期筛选
    ordering = ['name']  # 排序方式
