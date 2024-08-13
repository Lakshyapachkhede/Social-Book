from django.shortcuts import render
from .models import Post
from django.views.generic import (
    ListView,
    DetailView
)

class PostListView(ListView):
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        text_posts = Post.objects.all()
        

        posts = sorted(
            list(text_posts),
            key=lambda x: x.date_posted,
            reverse=True
        )

        return posts
    
    
class PostDetailView(DetailView):
    model = Post

