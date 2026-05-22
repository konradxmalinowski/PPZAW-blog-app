from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.account_settings, name='settings'),
    path('settings/password/', views.change_password, name='change_password'),
    path('settings/email/', views.change_email, name='change_email'),
    path('settings/2fa/setup/', views.setup_2fa, name='setup_2fa'),
    path('settings/2fa/disable/', views.disable_2fa, name='disable_2fa'),
    path('settings/2fa/backup-codes/', views.show_backup_codes, name='show_backup_codes'),
    path('settings/2fa/backup-codes/regenerate/', views.regenerate_backup_codes, name='regenerate_backup_codes'),
    path('2fa/verify/', views.verify_2fa, name='verify_2fa'),
    path('verify-email/sent/', views.verify_email_sent, name='verify_email_sent'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='registration/password_reset_email.txt',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/accounts/password-reset/done/',
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/password-reset/complete/',
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('<str:username>/', views.public_profile, name='public_profile'),
]
