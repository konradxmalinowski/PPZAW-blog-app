import secrets
import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import models
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
    notify_comments = models.BooleanField(default=True)

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
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    profile.save()


class EmailVerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        from datetime import timedelta
        from django.utils.timezone import now
        return not self.used and (now() - self.created_at) < timedelta(hours=24)


class TwoFactorBackupCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='backup_codes')
    code_hash = models.CharField(max_length=128)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_for_user(cls, user, count=8):
        cls.objects.filter(user=user).delete()
        codes = []
        for _ in range(count):
            code = secrets.token_hex(5).upper()
            cls.objects.create(user=user, code_hash=make_password(code))
            codes.append(code)
        return codes

    @classmethod
    def verify_and_consume(cls, user, code):
        submitted = code.strip().upper()
        for backup in cls.objects.filter(user=user, used=False):
            if check_password(submitted, backup.code_hash):
                backup.used = True
                backup.save()
                return True
        return False


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('password_change', 'Password Change'),
        ('email_change', 'Email Change'),
        ('2fa_enabled', '2FA Enabled'),
        ('2fa_disabled', '2FA Disabled'),
        ('2fa_failed', '2FA Failed'),
        ('backup_code_used', 'Backup Code Used'),
        ('register', 'Register'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
