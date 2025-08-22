from django.db.models import MultipleObjectsReturned
from .models import Cart

def cart(request):
    cart_obj = None
    try:
        if request.user.is_authenticated:
            # 若有多个，取最新的并删除旧的
            carts = Cart.objects.filter(user=request.user).order_by('-updated_at')
            if len(carts) > 1:
                for cart in carts[1:]:
                    cart.delete()
                cart_obj = carts[0]
            else:
                cart_obj, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_id = request.session.session_key or request.session.create()
            carts = Cart.objects.filter(session_id=session_id).order_by('-updated_at')
            if len(carts) > 1:
                for cart in carts[1:]:
                    cart.delete()
                cart_obj = carts[0]
            else:
                cart_obj, created = Cart.objects.get_or_create(session_id=session_id)
    except MultipleObjectsReturned:
        # 极端情况：强制清理重复项
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).exclude(id=carts.first().id).delete()
            cart_obj = carts.first()
        else:
            Cart.objects.filter(session_id=session_id).exclude(id=carts.first().id).delete()
            cart_obj = carts.first()
    return {'cart': cart_obj}