from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': '댓글을 입력하세요...'
        }),
        label='댓글'
    )

    class Meta:
        model = Comment
        fields = ['content']   # 유저가 직접 입력하는 필드만!