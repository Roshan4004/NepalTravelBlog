
from django.forms import ImageField, ModelForm,TextInput, Textarea
from .models import Post,Comment
from tinymce.widgets import TinyMCE
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget 

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