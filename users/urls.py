from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, email_verification, password_recovery, UserListView, UserProfileModeratorView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('password_recovery/', password_recovery, name='password_recovery'),
    path('users/', UserListView.as_view(), name='users'),
    path('user_activation/<int:pk>', UserProfileModeratorView.as_view(template_name='users/user_activation.html'),
         name='user_activation'),
]
