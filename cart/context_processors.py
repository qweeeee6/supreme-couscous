from .models import Cart


def cart(request):
    """
    上下文处理器：在所有模板中提供购物车信息
    """
    # 尝试获取当前用户的购物车
    if request.user.is_authenticated:
        cart_obj, created = Cart.objects.get_or_create(user=request.user)
    else:
        # 匿名用户使用session_id
        session_id = request.session.session_key
        if not session_id:
            request.session.save()
            session_id = request.session.session_key
        cart_obj, created = Cart.objects.get_or_create(session_id=session_id)

    return {'cart': cart_obj}
