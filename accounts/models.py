# accounts/models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from products.models import Product

class Favorite(models.Model):
    """用户收藏模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ('user', 'product')  # 确保用户不会重复收藏同一商品

    def __str__(self):
        return f"{self.user.username} 收藏了 {self.product.name}"

class UserProfile(models.Model):
    """用户资料扩展，区分普通用户和商户"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_merchant = models.BooleanField(default=False, verbose_name="是否为商户")
    merchant_application = models.BooleanField(default=False, verbose_name="是否申请成为商户")
    merchant_approved = models.BooleanField(default=False, verbose_name="商户申请是否通过")
    # 商户额外信息
    store_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="店铺名称")
    store_description = models.TextField(blank=True, null=True, verbose_name="店铺描述")
    # 其他可选信息：营业执照、联系方式等

    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"