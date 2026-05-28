from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Board, Post, Comment, Like
from .forms import CommentForm, PostForm, CustomUserCreationForm
from django.contrib.auth import logout as auth_logout


# =====================
# 회원 관련
# =====================

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('cp_everytime:board_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cp_everytime/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('cp_everytime:board_list')
    else:
        form = AuthenticationForm()
    return render(request, 'cp_everytime/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('cp_everytime:board_list')


@login_required
def mypage_view(request):
    user = request.user
    my_posts = Post.objects.filter(author=user).order_by('-created_at')
    my_comments = Comment.objects.filter(author=user).order_by('-created_at')
    my_likes = Post.objects.filter(likes__user=user).order_by('-created_at')

    return render(request, 'cp_everytime/mypage.html', {
        'user': user,
        'nickname': user.username,
        'my_posts': my_posts,
        'my_comments': my_comments,
        'my_likes': my_likes,
    })


# =====================
# 게시판 관련
# =====================

def board_list(request):
    boards = Board.objects.annotate(post_count=Count('post'))
    popular_posts = Post.objects.all().order_by('-created_at')[:5]
    return render(request, 'cp_everytime/board_list.html', {
        'boards': boards,
        'popular_posts': popular_posts,
    })


def post_list(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    posts_list = Post.objects.filter(board=board).order_by('-created_at')

    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    posts = Paginator(posts_list, 20).get_page(request.GET.get('page'))
    return render(request, 'cp_everytime/post_list.html', {'board': board, 'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, 'cp_everytime/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def post_create(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.board = board
            post.is_anonymous = request.POST.get('is_anonymous') == 'on'
            post.save()
            return redirect('cp_everytime:post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'cp_everytime/post_form.html', {'form': form, 'board': board})


@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.author:
        return redirect('cp_everytime:post_detail', id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.is_anonymous = request.POST.get('is_anonymous') == 'on'
            post.save()
            return redirect('cp_everytime:post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'cp_everytime/post_form.html', {'form': form, 'post': post, 'board': post.board})


@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    board_id = post.board.id
    if request.user == post.author:
        post.delete()
    return redirect('cp_everytime:post_list', board_id=board_id)


# =====================
# 댓글 / 좋아요
# =====================

@login_required
def comment_create(request, post_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.author = request.user
            comment.save()
    return redirect('cp_everytime:post_detail', id=post_id)


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        comment.delete()
    return redirect('cp_everytime:post_detail', id=post_id)


@login_required
def like_toggle(request, post_id):
    like, created = Like.objects.get_or_create(
        post_id=post_id,
        user=request.user,
    )
    if not created:
        like.delete()
    return redirect('cp_everytime:post_detail', id=post_id)