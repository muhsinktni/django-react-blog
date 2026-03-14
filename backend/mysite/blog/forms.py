from django import forms
from .models import Post, Tag, Comment
import re


class ContactForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your message')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags' ]
        labels = {
            'title': 'Enter a title here',
            'content': 'Write your content here'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your content here'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


        # Clean title
    def clean_title(self):
        title = self.cleaned_data.get("title")

        # # 1️⃣ Unique title (case-insensitive)
        # if Post.objects.filter(title__iexact=title).exists():
        #     raise forms.ValidationError("A post with this title already exists.")

        # 3️⃣ No emojis in title
        if contains_emoji(title):
            raise forms.ValidationError("Title cannot contain emojis.")

        # 4️⃣ No repeated consecutive words
        if has_repeated_words(title):
            raise forms.ValidationError("Title contains repeated words.")

        return title

    # Clean content
    def clean_content(self):
        content = self.cleaned_data.get("content")

        # 2️⃣ Minimum 100 characters
        # if len(content) < 100:
        #     raise forms.ValidationError("Content must be at least 100 characters long.")

        # 3️⃣ No emojis
        if contains_emoji(content):
            raise forms.ValidationError("Content cannot contain emojis.")

        # 4️⃣ No repeated consecutive words
        if has_repeated_words(content):
            raise forms.ValidationError("Content contains repeated words.")

        return content

    # Clean whole form
    def clean(self):
        cleaned = super().clean()

        # 5️⃣ Tags cannot be empty
        tags = cleaned.get("tags")
        if not tags:
            raise forms.ValidationError("You must select at least one tag.")

        return cleaned


# ---------------------------------------------------
# Helper function: detect emojis
def contains_emoji(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "]+",
        flags=re.UNICODE
    )
    return bool(emoji_pattern.search(text))


# Helper: detect repeated consecutive words
def has_repeated_words(text):
    words = text.lower().split()
    for i in range(len(words) - 1):
        if words[i] == words[i+1]:
            return True
    return False





class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

# class AuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['name', 'place']
#         widgets ={
#             'name': forms.TextInput(attrs={'class': 'form-control'}),
#             'place': forms.TextInput()
#         }




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']