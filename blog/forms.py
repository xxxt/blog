from django import forms

from blog.models import Blog


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'body', 'category', 'tags')
