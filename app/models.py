from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User_Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    image=models.ImageField()
    email=models.EmailField()
    phone=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField()
    group = models.ForeignKey('Group',on_delete=models.CASCADE)
    sender = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    def __str__(self):
        return self.group.name

class Group(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    background=models.ImageField()
    created_by = models.CharField(max_length=100,default="admin")
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.name

class User_Group(models.Model):
    user=models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    status=models.BooleanField()
    def __str__(self):
        return self.user.user.username

