from django import template
from django.forms.boundfield import BoundField

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    为表单字段添加CSS类，兼容普通字段和复选框等特殊字段
    """
    # 检查是否是表单字段对象
    if isinstance(field, BoundField):
        # 处理常规表单字段
        attrs = field.field.widget.attrs.copy()
        if 'class' in attrs:
            attrs['class'] += ' ' + css_class
        else:
            attrs['class'] = css_class
        return field.as_widget(attrs=attrs)
    else:
        # 处理字符串形式的字段（如复选框标签）
        # 直接返回原始内容，不添加类
        return field
