from django.contrib import admin
from apps.accounts.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'github_url', 'website')
    search_fields = ('user__username', 'bio')
