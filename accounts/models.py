from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def get_default_profile_image():
    return 'userimage/user-icon.png'

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    country=models.TextField(blank=False)
    local_address=models.TextField(blank=True,null=True)
    bio=models.TextField(blank=True)
    profile_img=models.ImageField(upload_to='userimage/',null=True,blank=True)

    def __str__(self):
        return self.user.username
    def get_pp(self):
        img=self.profile_img
        if img:
            return 'media/'+str(img)
        else:
            return 'media/userimage/user-icon.png'