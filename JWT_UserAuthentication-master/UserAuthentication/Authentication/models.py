from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    access_token_expiration=models.DateTimeField()
    refresh_token_expiration=models.DateTimeField()


    def __str__(self):
        return f" Tokens for {self.user.username}"