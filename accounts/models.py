from statistics import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    country=models.TextField(blank=False)
    local_address=models.TextField(blank=True,null=True)
    bio=models.TextField(blank=True)
    profile_img=models.ImageField(default='userimage/user-icon.png',upload_to='userimage/')

    def __str__(self):
        return self.user.username