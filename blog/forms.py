
from django.forms import  ModelForm, Textarea
from .models import Post,Comment
from django import forms
from django_summernote.widgets import SummernoteWidget

class PostForm(ModelForm):
    content = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%','placeholder':'Start typing..','border-color':'black','border-style':'solid','max-width':'100%'}}))
    class Meta:
        model = Post
        fields = ['content']
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': Textarea(attrs={
                'placeholder': 'Comment',
                'tag':'Comment',
                })
                }