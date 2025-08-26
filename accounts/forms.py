from django import forms
from django.contrib.auth.forms import UserCreationForm
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