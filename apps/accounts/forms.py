from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(label='Nowy e-mail')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError('Ten adres e-mail jest już zajęty.')
        return email

    def save(self):
        self.user.email = self.cleaned_data['email']
        self.user.save()
        return self.user


class TOTPVerifyForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        label='Kod weryfikacyjny',
        widget=forms.TextInput(attrs={'autocomplete': 'one-time-code', 'inputmode': 'numeric', 'pattern': '[0-9]*'}),
    )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Imię')
    last_name = forms.CharField(max_length=30, required=False, label='Nazwisko')

    class Meta:
        model = UserProfile
        fields = ('bio', 'avatar', 'github_url', 'website', 'notify_comments')
        labels = {
            'bio': 'Bio',
            'avatar': 'Avatar',
            'github_url': 'GitHub URL',
            'website': 'Strona WWW',
            'notify_comments': 'Powiadomienia e-mail o komentarzach',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data['first_name']
        profile.user.last_name = self.cleaned_data['last_name']
        profile.user.save()
        if commit:
            profile.save()
        return profile
