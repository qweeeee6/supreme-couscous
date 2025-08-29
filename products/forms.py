from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': '请输入您的评价...'}),
            'rating': forms.Select(attrs={'class': 'form-select'}),
        }