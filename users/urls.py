from django.urls import path
from.views import register, logout_view, ProfileDetailView, ProfileUpdateView, NotificationListView, send_friend_request, accept_friend_request, reject_friend_request, search, delete_friend_request, un_friend
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('search/', search, name='search'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('send-friend-request/<int:user_id>', send_friend_request, name='send-friend-request'),
    path('accept-friend-request/<int:request_id>', accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/<int:request_id>', reject_friend_request, name='reject-friend-request'),
    path('delete-friend-request/<int:request_id>', delete_friend_request, name='delete-friend-request'),
    path('un_friend/<int:user_id>', un_friend, name='un-friend'),
    path('profile<str:username>/friends'),


]
