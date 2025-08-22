from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import Cart


@login_required
def order_create(request):
    """创建订单"""
    # 获取当前用户的购物车
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            # 匿名用户应该已经登录，这里做个保护
            messages.error(request, '请先登录再结算')
            return redirect('login')

        if not cart.items.exists():
            messages.warning(request, '您的购物车是空的，无法创建订单')
            return redirect('cart:cart_detail')

    except Cart.DoesNotExist:
        messages.warning(request, '您的购物车是空的，无法创建订单')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        # 创建订单
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            city=request.POST.get('city'),
            phone=request.POST.get('phone'),
            total_price=cart.get_total_price()
        )

        # 创建订单项
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

            # 减少库存
            item.product.stock -= item.quantity
            if item.product.stock == 0:
                item.product.available = False
            item.product.save()

        # 清空购物车
        cart.items.all().delete()

        messages.success(request, '订单创建成功！')
        return redirect('orders:order_detail', order_id=order.id)

    # GET请求显示订单创建表单
    return render(request, 'orders/order_create.html', {
        'cart': cart
    })


@login_required
def order_list(request):
    """用户订单列表"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    """订单详情"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order
    })
