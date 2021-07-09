from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserTable(models.Model):
    FirstName = models.CharField(null=True,max_length=255)
    LastName = models.CharField(null=True,max_length=255)
    Email = models.CharField(null=True,max_length=255)
    Password = models.CharField(null=True,max_length=255)
    User = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)


    def __str__(self):
        return self.Email