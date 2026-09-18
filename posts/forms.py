from django import forms

from posts.models import Post


BANNED_WORDS = ('war', 'ban', 'begin')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'category', 'image', 'tags')

    def clean_title(self):
        title = self.cleaned_data['title']

        for banned_word in BANNED_WORDS:
            if banned_word in title.casefold():
                raise forms.ValidationError(
                    f'Слово "{banned_word}" запрещено в заголовке.'
                )

        return title
