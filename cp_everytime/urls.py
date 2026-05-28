from django.urls import path
from . import views

app_name = 'cp_everytime'

urlpatterns = [
    path('<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:post_id>/like/', views.like_toggle, name='like_toggle'),
]