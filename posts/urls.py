from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post-home'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', views.like_post, name="like-post"),
    path('post/<int:pk>/comment/', views.add_comment, name="comment-post"),
    path('post/<int:pk>/comment/delete', views.delete_comment, name="comment-delete"),
    path('post/share/<int:post_id>', views.share_post, name="post-share")

]
