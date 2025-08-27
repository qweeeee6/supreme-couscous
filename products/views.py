from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.db.models import Q
from decimal import Decimal, InvalidOperation


class ProductListView(ListView):
    """产品列表视图（增强版，支持多条件筛选）"""
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug = self.kwargs.get('category_slug')

        # 1. 分类筛选
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None

        # 2. 关键词搜索（支持名称和描述）
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # 3. 价格区间筛选
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        try:
            if min_price:
                queryset = queryset.filter(price__gte=Decimal(min_price))
            if max_price:
                queryset = queryset.filter(price__lte=Decimal(max_price))
        except InvalidOperation:
            # 处理无效价格输入
            pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.category
        # 将当前筛选参数传递到模板（用于保持表单状态）
        context['current_filters'] = self.request.GET.dict()
        return context

class ProductDetailView(DetailView):
    """产品详情视图"""
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取相关产品（同类别）
        product = self.get_object()
        context['related_products'] = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id)[:4]

        if self.request.user.is_authenticated:
            from accounts.models import Favorite  # 导入收藏模型
            context['user_favorites'] = Favorite.objects.filter(
                user=self.request.user,
                product=product
            ).exists()

        return context
