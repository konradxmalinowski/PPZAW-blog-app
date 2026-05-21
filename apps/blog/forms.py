from django import forms

from apps.blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={'placeholder': 'Twoje imie'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'twoj@email.com'}),
    )
    to = forms.EmailField(
        label='Do (e-mail odbiorcy)',
        widget=forms.EmailInput(attrs={'placeholder': 'odbiorca@email.com'}),
    )
    comments = forms.CharField(
        required=False,
        label='Komentarz (opcjonalny)',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': '// opcjonalna wiadomosc...'}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Twoja nazwa'}),
            'email': forms.EmailInput(attrs={'placeholder': 'twoj@email.com'}),
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': '// Twoj komentarz...',
            }),
        }
        labels = {
            'name': 'Nazwa',
            'email': 'E-mail',
            'body': 'Komentarz',
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        label='Szukaj',
        widget=forms.TextInput(attrs={
            'placeholder': '$ grep -r "..." ./posts/',
            'autofocus': True,
        }),
    )
