from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


@require_POST
def cart_add(request, product_id):
    """添加商品到购物车（支持自定义数量）"""
    product = get_object_or_404(Product, id=product_id)

    # 读取前端传入的数量（默认为1，确保是整数且不小于1）
    try:
        quantity = int(request.POST.get('quantity', 1))
        quantity = max(1, quantity)  # 确保数量至少为1
    except (ValueError, TypeError):
        quantity = 1  # 转换失败时默认1

    # 检查数量是否超过库存
    if quantity > product.stock:
        messages.error(request, f'抱歉，{product.name} 库存不足（当前库存：{product.stock}）')
        return redirect('products:product_detail', id=product.id, slug=product.slug)

    # 获取或创建购物车（原有逻辑不变）
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    # 处理购物车项：使用传入的quantity更新数量
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # 更新为传入的数量（而非+1）
        if cart_item.quantity + quantity <= product.stock:
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'已将 {product.name} 的数量更新为 {cart_item.quantity}')
        else:
            messages.error(request, f'抱歉，{product.name} 库存不足（当前库存：{product.stock}）')
    except CartItem.DoesNotExist:
        # 创建新订单项时使用传入的quantity
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f'已将 {product.name} 添加到购物车（数量：{quantity}）')

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
