from statistics import mode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_tokens=models.CharField(max_length=150 )
    is_verified=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username