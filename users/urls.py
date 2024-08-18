from django.urls import path
from.views import register, logout_view, ProfileDetailView, ProfileUpdateView, NotificationListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/<str:username>/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),

]
