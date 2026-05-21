from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.accounts.forms import RegisterForm, UserProfileForm
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
    # get_or_create handles superuser/legacy users without a profile
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
