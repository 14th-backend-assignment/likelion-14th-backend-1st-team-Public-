# cp_everytime/urls.py
from django.urls import path
from . import views

app_name = 'cp_everytime'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),    # /accounts/signup/
    path('login/', views.login_view, name='login'),      # /accounts/login/
    path('mypage/', views.profile_view, name='profile'),    # /accounts/mypage/
]