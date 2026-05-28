# cp_everytime/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# 1. 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # 회원가입 성공하면 장고 기본 프로필(내 정보) 페이지로 이동
            return redirect('/accounts/profile/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# 2. 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # 로그인 성공하면 장고 기본 프로필(내 정보) 페이지로 이동
            return redirect('/accounts/profile/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# 4. 내 정보 (마이페이지) 뷰
@login_required
def profile_view(request):
    user = request.user
    context = {
        'user': user,
        'nickname': user.username,
    }
    return render(request, 'mypage.html', context)