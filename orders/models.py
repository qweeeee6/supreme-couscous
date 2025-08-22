from django.db import models
from django.conf import settings
from products.models import Product


class Order(models.Model):
    """订单模型"""
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('paid', '已支付'),
        ('shipped', '已发货'),
        ('delivered', '已送达'),
        ('cancelled', '已取消'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders',
                             verbose_name="用户")
    first_name = models.CharField(max_length=100, verbose_name="名")
    last_name = models.CharField(max_length=100, verbose_name="姓")
    email = models.EmailField(verbose_name="邮箱")
    address = models.CharField(max_length=250, verbose_name="地址")
    postal_code = models.CharField(max_length=20, verbose_name="邮政编码")
    city = models.CharField(max_length=100, verbose_name="城市")
    phone = models.CharField(max_length=20, verbose_name="电话")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="订单总价")

    class Meta:
        ordering = ['-created_at']
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    """订单项模型"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="订单")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="产品")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量")

    class Meta:
        verbose_name = '订单项'
        verbose_name_plural = '订单项'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """计算单项总价"""
        return self.price * self.quantity
