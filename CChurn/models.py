from django.db import models
from Account.models import UserTable
# Create your models here.
class FormDataFile(models.Model):
    File = models.FileField(null = True,blank= True)
    UserID = models.ForeignKey(UserTable,on_delete=models.CASCADE,blank=True,null=True)
    DateImputed = models.DateTimeField(null=True,blank=True)