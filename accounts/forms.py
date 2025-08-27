from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    """用户注册表单，继承自Django内置的UserCreationForm"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    # 其他字段（用户名、密码）...
    remember_me = forms.BooleanField(
        required=False,  # 可选，不勾选也能提交
        label="记住我"
    )

class RegistrationForm(UserCreationForm):
    """扩展注册表单，增加姓名字段"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="名")
    last_name = forms.CharField(max_length=30, required=True, label="姓")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class UserProfileForm(UserChangeForm):
    """个人资料编辑表单"""
    password = None  # 排除密码字段（单独处理）
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': '名',
            'last_name': '姓',
        }