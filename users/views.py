from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth import logout, login
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .models import Profile, Notification
from django.views.generic import (
    DetailView,
    UpdateView,
    ListView
)
from posts.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse



def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post-home')
        
    else:
        form = forms.UserRegisterForm()

    return render(request, 'users/register.html', {'form':form})
            
@login_required
@require_GET
def logout_view(request):
    logout(request)

    return render(request, 'users/logout.html')

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(Profile, user__username=username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        current_user_profile = Profile.objects.get(user=self.request.user)
        context['mutual_friends_count'] = current_user_profile.mutual_friends(profile)
        context['posts'] = Post.objects.filter(author=profile.user).order_by('-date_posted')

        # for getting latest six images posted by profile user
        user_posts = Post.objects.filter(author=profile.user)
        
        images = []
        for post in user_posts:
            images.extend(post.images.all())
        latest_images = sorted(images, key=lambda image: image.photo_post.first().date_posted, reverse=True)[:6]
        context['post_photos'] = latest_images
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ["intro", "banner_image", "user_image", "works", "education", "home", "location"]

    def get_object(self):
        username = self.kwargs['username']
        return Profile.objects.get(user=User.objects.filter(username=username).first())

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.get_object().user.username})
    
    def form_valid(self, form):
        print("\n", self.request.FILES) 
        return super().form_valid(form)
    


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by('-timestamp')



