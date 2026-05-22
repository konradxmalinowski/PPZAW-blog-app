from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    github_url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    totp_secret = models.CharField(max_length=32, blank=True)
    two_factor_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'Profil {self.user.username}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('accounts:public_profile', args=[self.user.username])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Use get_or_create to handle existing users (e.g. superuser created before this signal)
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    profile.save()
