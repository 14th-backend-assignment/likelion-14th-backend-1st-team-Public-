like
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Comment, Like
from .forms import CommentForm


@login_required
def comment_create(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.author = request.user
            comment.save()
    return redirect('post:detail', post_id)

@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('post:detail', post_id)

@login_required
def like_toggle(request, post_id):
    like, created = Like.objects.get_or_create(
        post_id=post_id,
        user=request.user,
    )
    if not created:
        like.delete()
    return redirect('post:detail', post_id)
good
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Board, Post
from .forms import PostForm

from django.shortcuts import render

def mypage_view(request):
    return render(request, 'cp_everytime/mypage.html')

# 1. 게시판 메인 페이지
def board_list(request):
    boards = Board.objects.annotate(post_count=Count('post'))
    
    # 'likes' 대신 'id'를 기준으로 정렬하거나, 좋아요 기능이 구현될 때까지 보류합니다.
    popular_posts = Post.objects.all().order_by('-created_at')[:5] 
    
    context = {
        'boards': boards,
        'popular_posts': popular_posts,
    }
    return render(request, 'cp_everytime/board_list.html', context)

# 2. 게시글 목록 페이지 (검색 & 페이징)
def post_list(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    
    # [수정된 부분] .annotate(...) 부분을 삭제했습니다.
    # 좋아요나 댓글 기능이 3번 담당자에 의해 구현되기 전까지는 이 부분을 빼야 합니다.
    posts_list = Post.objects.filter(board=board).order_by('-created_at')

    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts_list, 20)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'cp_everytime/post_list.html', {'board': board, 'posts': posts})

# 3. 게시글 작성
@login_required
def post_create(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.board = board
            # 체크박스 값 처리 (True/False 저장)
            post.is_anonymous = request.POST.get('is_anonymous') == 'on'
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'cp_everytime/post_form.html', {'form': form, 'board': board})

# 4. 게시글 수정
@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    # 작성자 본인만 수정 가능하게 방어 코드
    if request.user != post.author:
        return redirect('post_detail', id=post.id)
        
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_anonymous = request.POST.get('is_anonymous') == 'on'
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'cp_everytime/post_form.html', {'form': form, 'post': post, 'board': post.board})

# 5. 게시글 삭제
@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user == post.author:
        post.delete()
    return redirect('post_list', board_id=post.board.id)

# 6. 게시글 상세 (3번 담당자와 공유)
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'cp_everytime/post_detail.html', {'post': post})
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
  main
main
