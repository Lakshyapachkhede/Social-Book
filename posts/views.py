from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Image, Like, Comment, Share
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from users.models import Notification
from django.contrib.contenttypes.models import ContentType


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user_profile = self.request.user.profile
        friends = user_profile.friends.all()
        friends_user = friends.values_list('user', flat=True)

        friends_posts = Post.objects.filter(
            Q(author__in=friends_user) | Q(shares__shared_by__in=friends_user)
        ).distinct().annotate(total_shares=Count('shares'), total_likes=Count('likes')).order_by('-date_posted')

        popular_posts = Post.objects.exclude(
            Q(author__in=friends_user) | Q(shares__shared_by__in=friends_user)
        ).annotate(
            total_shares=Count('shares'), total_likes=Count('likes')
        ).order_by("-total_likes", "-total_shares", "-date_posted")

       
        posts = list(friends_posts) + list(popular_posts)

        return posts

    
    
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['caption', 'images']
    success_url = reverse_lazy('post-home')

    def form_valid(self, form):
        form.instance.author = self.request.user

        post = form.save(commit=False)
        post.save()
        images = self.request.FILES.getlist('images')
        if images:
            for image_file in images:
                image = Image.objects.create(image=image_file)
                post.images.add(image)
        

        post.save()
        return redirect(self.success_url)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["caption", "images"]


    def form_valid(self, form):
        form.instance.author = self.request.user

        post = form.save(commit=False)
        post.save()
        images = self.request.FILES.getlist('images')
        if images:
            for image_file in images:
                image = Image.objects.create(image=image_file)
                post.images.add(image)
        

        post.save()
        return redirect(self.success_url)

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        return self.get_object().author == self.request.user



@require_POST
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if Like.objects.filter(post=post, author=user).exists():
        Like.objects.filter(post=post, author=user).delete()
        liked = False
    else:
        Like.objects.create(post=post, author=user)
        liked = True
        if request.user != post.author:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type='LK',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id
            )

    return JsonResponse({
        'liked':liked,
        'likes_count':post.likes.count(),
    })

@login_required  
def add_comment(request, pk):
    post = Post.objects.get(id=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        if request.user != post.author:
            Notification.objects.create(
                sender=request.user,
                receiver=post.author,
                notification_type='CM',
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post.id
            )
    
    return redirect('post-detail', pk=pk)



@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.author == request.user:
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post-detail', pk=post_pk)


@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not Share.objects.filter(post=post, shared_by=request.user).exists():
        Share.objects.create(
            post=post,
            shared_by=request.user
        )

        return JsonResponse({
            'shared':True,
            'totalShares':post.shares.count(),
        })
    
    return JsonResponse({
            'shared':False,
            'totalShares':post.shares.count(),
        })
