from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@require_POST
def cart_add(request, product_id):
    """添加商品到购物车"""
    product = get_object_or_404(Product, id=product_id)

    # 获取或创建购物车
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    # 尝试获取已有购物车项
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'已将 {product.name} 的数量更新为 {cart_item.quantity}')
    except CartItem.DoesNotExist:
        # 创建新的购物车项
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, f'已将 {product.name} 添加到购物车')

    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    """从购物车移除商品"""
    cart_item = get_object_or_404(CartItem, id=item_id)

    # 验证购物车归属
    if request.user.is_authenticated:
        if cart_item.cart.user != request.user:
            messages.error(request, '无权操作此购物车')
            return redirect('cart:cart_detail')
    else:
        session_id = request.session.session_key
        if cart_item.cart.session_id != session_id:
            messages.error(request, '无权操作此购物车')
            return redirect('cart:cart_detail')

    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'已从购物车中移除 {product_name}')
    return redirect('cart:cart_detail')


def cart_detail(request):
    """查看购物车详情"""
    # 获取当前用户的购物车
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    return render(request, 'cart/cart_detail.html', {'cart': cart})
