from django.urls import path
from django.contrib.auth import views as auth_views
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
    path('2fa/verify/', views.verify_2fa, name='verify_2fa'),
    path('<str:username>/', views.public_profile, name='public_profile'),
]
