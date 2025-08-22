from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """购物车模型"""
    """购物车模型"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="用户", unique=True)  # 添加unique=True
    session_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="会话ID",
                                  unique=True)  # 添加unique=True
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = '购物车'

        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(session_id__isnull=False),
                name="cart_user_or_session_required"
            )
        ]

    def __str__(self):
        return f"Cart {self.id}"

    def get_total_price(self):
        """计算购物车总价"""
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    """购物车项目模型"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name="购物车")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = '购物车项目'
        verbose_name_plural = '购物车项目'
        # 约束：同一购物车中同一商品只能有一条记录（避免重复添加）
        unique_together = ['cart', 'product']  # 关键添加

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """计算单项总价"""
        return self.product.price * self.quantity
