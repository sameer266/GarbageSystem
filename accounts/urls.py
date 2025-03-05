from django.urls import path
from accounts.views import (UserRegistrationView,
                            UserLoginView,
                            UserListView,
                            UserProfileView,
                            UserChangePasswordView,
                            SendPasswordResetEmailView,
                            UserPasswordResetView,
                            LogoutView,
                            OTPValidation,
                            AboutUsView,
                            UserRewardViews,
                            SocialRegisterLoginView
                            )      

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('list', UserListView.as_view(), name='userlist'), #user list
 
    #login
    path('register',UserRegistrationView.as_view(), name='register'),
    path('login',UserLoginView.as_view(), name='register'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('update/profile', UserProfileView.as_view(), name='profile'),
    path('change/password', UserChangePasswordView.as_view(), name='changepassword'),
    path('forgot/password', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset/password/<uid>/<token>', UserPasswordResetView.as_view(), name='reset-password'),
   
    path('otp',OTPValidation.as_view(), name="otp"),
    path('reset/password', UserPasswordResetView.as_view(), name='reset-password'),
    path('logout', LogoutView.as_view(), name='logout'),
    
    path('aboutus', AboutUsView.as_view(),name='aboutus'),
    path('reward', UserRewardViews.as_view(), name='reward_points'),
    path('social/login-register', SocialRegisterLoginView.as_view(), name ="social_register"),
]