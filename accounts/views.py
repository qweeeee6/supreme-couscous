from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, UserProfileForm
from .models import Favorite
from products.models import Product


def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'账号 {username} 创建成功，请登录！')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    """用户个人资料视图"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """编辑个人资料视图"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {
        'form': form
    })


@login_required
def password_change(request):
    """密码修改视图"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 更新会话，避免密码修改后退出登录
            update_session_auth_hash(request, user)
            messages.success(request, '密码修改成功！')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/password_change.html', {
        'form': form
    })


@login_required
def favorite_toggle(request, product_id):
    """添加/移除收藏"""
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        message = f'已取消收藏 {product.name}'
        is_favorited = False
    else:
        message = f'已收藏 {product.name}'
        is_favorited = True

    # 处理AJAX请求
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': message,
            'is_favorited': is_favorited
        })

    messages.success(request, message)
    return redirect('accounts:favorite_list')


@login_required
def favorite_list(request):
    """我的收藏列表"""
    favorites = Favorite.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'accounts/favorites.html', {
        'favorites': favorites,
        'title': '我的收藏'
    })