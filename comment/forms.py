from django import forms
from .models import Comment
# Create your views here.


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']