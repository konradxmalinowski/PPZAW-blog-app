import base64
import io
import pyotp
import qrcode

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from apps.accounts.forms import RegisterForm, UserProfileForm, ChangeEmailForm, TOTPVerifyForm
from apps.accounts.models import UserProfile
from apps.blog.models import Post


def register(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    posts = Post.published.filter(author=request.user).order_by('-publish')
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'posts': posts,
    })


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    posts = Post.published.filter(author=user).order_by('-publish')
    return render(request, 'accounts/public_profile.html', {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
    })


@login_required
def account_settings(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/settings.html', {'profile': profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Hasło zostało zmienione.')
            return redirect('accounts:settings')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adres e-mail został zmieniony.')
            return redirect('accounts:settings')
    else:
        form = ChangeEmailForm(request.user)
    return render(request, 'accounts/change_email.html', {'form': form})


@login_required
def setup_2fa(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if profile.two_factor_enabled:
        return redirect('accounts:settings')

    if not profile.totp_secret:
        profile.totp_secret = pyotp.random_base32()
        profile.save()

    totp = pyotp.TOTP(profile.totp_secret)
    otp_uri = totp.provisioning_uri(
        name=request.user.email or request.user.username,
        issuer_name='DevLog',
    )

    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(otp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            if totp.verify(form.cleaned_data['code']):
                profile.two_factor_enabled = True
                profile.save()
                request.session['2fa_verified'] = True
                messages.success(request, 'Weryfikacja dwuetapowa została włączona.')
                return redirect('accounts:settings')
            else:
                form.add_error('code', 'Nieprawidłowy kod. Spróbuj ponownie.')
    else:
        form = TOTPVerifyForm()

    return render(request, 'accounts/setup_2fa.html', {
        'form': form,
        'qr_b64': qr_b64,
        'secret': profile.totp_secret,
    })


@login_required
def disable_2fa(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            totp = pyotp.TOTP(profile.totp_secret)
            if totp.verify(form.cleaned_data['code']):
                profile.two_factor_enabled = False
                profile.totp_secret = ''
                profile.save()
                request.session.pop('2fa_verified', None)
                messages.success(request, 'Weryfikacja dwuetapowa została wyłączona.')
                return redirect('accounts:settings')
            else:
                form.add_error('code', 'Nieprawidłowy kod.')
    else:
        form = TOTPVerifyForm()
    return render(request, 'accounts/disable_2fa.html', {'form': form})


def verify_2fa(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if not profile.two_factor_enabled:
        return redirect('blog:post_list')

    next_url = request.GET.get('next') or request.POST.get('next') or '/'

    if request.method == 'POST':
        form = TOTPVerifyForm(request.POST)
        if form.is_valid():
            totp = pyotp.TOTP(profile.totp_secret)
            if totp.verify(form.cleaned_data['code']):
                request.session['2fa_verified'] = True
                return redirect(next_url)
            else:
                form.add_error('code', 'Nieprawidłowy kod.')
    else:
        form = TOTPVerifyForm()

    return render(request, 'accounts/verify_2fa.html', {'form': form, 'next': next_url})
