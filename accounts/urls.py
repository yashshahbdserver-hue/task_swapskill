from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/complete/', views.ProfileCompleteView.as_view(), name='profile_complete'),
    
    # Password management
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name='password_change_done'),
    
    # Email verification
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('verify-email/sent/', views.EmailVerificationSentView.as_view(), name='email_verification_sent'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='verify_otp'),
    path('reset-password/', views.PasswordResetView.as_view(), name='reset_password'),
    
    # AJAX endpoints
    path('ajax/get-branches/', views.get_branches, name='get_branches'),
]