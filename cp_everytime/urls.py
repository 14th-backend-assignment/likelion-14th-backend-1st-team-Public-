from django.urls import path
from . import views

app_name = 'cp_everytime'

urlpatterns = [
    # 게시판 메인
    path('board/', views.board_list, name='board_list'),
    
    # 게시글 목록 (board_id 사용)
    path('board/<int:board_id>/', views.post_list, name='post_list'),
    
    # 게시글 상세
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    
    # 글 작성 (board_id 전달)
    path('post/new/<int:board_id>/', views.post_create, name='post_create'),
    
    # 글 수정
    path('post/edit/<int:id>/', views.post_update, name='post_update'),
    path('mypage/', views.mypage_view, name='mypage'),
    path('<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_id>/like/', views.like_toggle, name='like_toggle'),
    path('signup/', views.signup_view, name='signup'),  # /accounts/signup/
    path('login/', views.login_view, name='login'),  # /accounts/login/
    path('mypage/', views.mypage_view, name='profile'),  # /accounts/mypage/
    path('logout/', views.logout_view, name='logout'),
    path('post/delete/<int:id>/', views.post_delete, name='post_delete'),
]
