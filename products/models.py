from django.db import models
from django.urls import reverse


class Category(models.Model):
    """零食类别模型"""
    name = models.CharField(max_length=200, verbose_name="类别名称")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL别名")
    description = models.TextField(blank=True, verbose_name="类别描述")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="类别图片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['name']
        verbose_name = '零食类别'
        verbose_name_plural = '零食类别'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """零食产品模型"""
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="所属类别")
    name = models.CharField(max_length=200, verbose_name="产品名称")
    slug = models.SlugField(max_length=200, unique_for_date='created_at', verbose_name="URL别名")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="产品图片")
    description = models.TextField(blank=True, verbose_name="产品描述")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")
    stock = models.PositiveIntegerField(verbose_name="库存数量")
    available = models.BooleanField(default=True, verbose_name="是否上架")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['name']
        verbose_name = '零食产品'
        verbose_name_plural = '零食产品'
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.id, self.slug])
