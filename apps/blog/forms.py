import bleach
from django import forms

from apps.blog.models import Comment, Post
from apps.blog.profanity import contains_profanity

ALLOWED_COMMENT_TAGS = ['b', 'i', 'em', 'strong', 'code', 'pre', 'a', 'p', 'br']
ALLOWED_COMMENT_ATTRS = {'a': ['href', 'title']}


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

    def clean_name(self):
        name = self.cleaned_data['name']
        if contains_profanity(name):
            raise forms.ValidationError('Nazwa zawiera niedozwolone słowa.')
        return name

    def clean_body(self):
        body = self.cleaned_data['body']
        clean = bleach.clean(body, tags=ALLOWED_COMMENT_TAGS, attributes=ALLOWED_COMMENT_ATTRS, strip=True)
        if contains_profanity(clean):
            raise forms.ValidationError('Komentarz zawiera niedozwolone słowa.')
        return clean


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        label='Szukaj',
        widget=forms.TextInput(attrs={
            'placeholder': '$ grep -r "..." ./posts/',
            'autofocus': True,
        }),
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'body', 'category', 'cover_image',
                  'cover_image_alt', 'status', 'meta_description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Tytuł posta'}),
            'slug': forms.TextInput(attrs={'placeholder': 'url-slug'}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Krótki opis...'}),
            'body': forms.Textarea(attrs={'rows': 20, 'id': 'post-body-editor'}),
            'meta_description': forms.TextInput(attrs={'placeholder': 'Meta description (max 160 znaków)'}),
        }
        labels = {
            'title': 'Tytuł',
            'slug': 'Slug URL',
            'excerpt': 'Fragment / opis',
            'body': 'Treść (Markdown)',
            'category': 'Kategoria',
            'cover_image': 'Zdjęcie nagłówkowe',
            'cover_image_alt': 'Alt tekst zdjęcia',
            'status': 'Status',
            'meta_description': 'Meta description',
        }
