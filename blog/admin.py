from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Comment, Post
# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    list_display = ('id','title','created','local_body')
    search_fields = ['title', 'content']
    summernote_fields = ('content',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)