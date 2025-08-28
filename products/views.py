from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .forms import ReviewForm
from .models import Product, Category, Review
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

    # products/views.py
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        product = self.object

        # 获取评论
        reviews = product.reviews.all()
        context['reviews'] = reviews

        # 计算各星级评论数量（1-5星）
        rating_counts = {i: 0 for i in range(1, 6)}  # 初始化1-5星的计数
        for review in reviews:
            if 1 <= review.rating <= 5:
                rating_counts[review.rating] += 1
        context['rating_counts'] = rating_counts  # 传递到模板

        # 计算平均评分
        if reviews:
            context['average_rating'] = sum(r.rating for r in reviews) / len(reviews)
        else:
            context['average_rating'] = 0

        return context

    def post(self, request, *args, **kwargs):
        # 关键步骤：手动获取产品对象并赋值给self.object
        self.object = self.get_object()  # 这行必须放在最前面

        # 处理评论表单
        form = ReviewForm(request.POST)
        if form.is_valid():
            # 检查用户是否已评论
            if Review.objects.filter(user=request.user, product=self.object).exists():
                messages.warning(request, '您已经评论过该商品')
                return redirect('products:product_detail', id=self.object.id, slug=self.object.slug)

            # 保存评论
            review = form.save(commit=False)
            review.product = self.object
            review.user = request.user
            review.save()

            messages.success(request, '评论提交成功！')
            return redirect('products:product_detail', id=self.object.id, slug=self.object.slug)
        else:
            # 表单无效时返回错误信息
            messages.error(request, '评论提交失败，请检查输入')
            # 获取上下文并传递错误表单
            context = self.get_context_data(object=self.object)
            context['review_form'] = form
            return self.render_to_response(context)
