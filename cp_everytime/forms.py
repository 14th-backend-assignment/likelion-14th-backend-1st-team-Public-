from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Post, User  # 커스텀 User 모델 import


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
        fields = ['content']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력하세요'
            }),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # 커스텀 User 모델 사용
        fields = ['username', 'email']