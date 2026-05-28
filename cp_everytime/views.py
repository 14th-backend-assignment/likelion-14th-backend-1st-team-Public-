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