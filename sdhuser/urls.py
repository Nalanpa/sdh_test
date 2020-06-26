"""
Urls for SDHTEST app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Signup, user_profile, top10, signup_confirm, email_activate

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='sdhuser/login.html'), name='login'),
    path('signup/', Signup.as_view(), name='signup'),
    path('signup_confirm/', signup_confirm, name='signup-confirm'),
    path('email_activate/<user_id>/<token>',
         email_activate, name='email-activate'),
    path('profile/', user_profile, name='user-profile'),
    path('top-10/', top10, name='top-10'),
]
