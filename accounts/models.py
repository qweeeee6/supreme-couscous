# accounts/models.py
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