from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/',views.ProductListView.as_view(),name='product_list_by_category'),
    path('<int:id>/<slug:slug>/',views.ProductDetailView.as_view(),name='product_detail'),
# 新增商品创建路由（通常只有商户/管理员可访问）
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
# 新增商户商品列表路由
    path('merchant/products/', views.MerchantProductListView.as_view(), name='merchant_products'),
]
