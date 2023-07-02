from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    title=models.TextField(max_length=50,unique=True)
    content=models.TextField(blank=False)
    # content=RichTextUploadingField()
    created=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posted_by")
    updated_on=models.DateTimeField(auto_now=True)
    local_body=models.TextField()
    local_name=models.TextField()
    main_img=models.ImageField(null=True,blank=True,unique=True,upload_to="uploads//")
    m_img_url=models.TextField(max_length=500,unique=False)
    images=models.FileField(null=True,blank=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like',blank=True)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        a=self.likes.count()
        if a>1:
            return (str(a)+" likes")
        elif a<1:
            return ("")
        else:
            return (str(a)+" like")
        # return self.likes.count()

    def styled_localbody(self):
        aa=self.local_body.split("(",1)
        return aa[0]

    def delete(self, using=None, keep_parents=False):
        # self.main_img.delete()
        super().delete()
    def number_of_comment(self):
        a=self.comments.count()
        if a>1:
            return (str(a)+" comments")
        elif a<1:
            return ("0")
        else:
            return (str(a)+" comment")
        # return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    cmnt_likes = models.ManyToManyField(User, related_name='comment_like',blank=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return '%s - %s' %(self.post.title, self.user.username)

    def number_of_comment_likes(self):
        a=self.cmnt_likes.count()
        if a>1:
            return (str(a)+" likes")
        elif a<1:
            return ("")
        else:
            return (str(a)+" like")
        # return self.cmnt_likes.count()

