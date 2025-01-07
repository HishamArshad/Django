from django.db import models
from authemail.models import EmailUserManager, EmailAbstractUser
from django.conf import settings

class MyUser(EmailAbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default.jpg')
    date_of_birth = models.DateField('Date of birth', null=True, blank=True)
    
    objects = EmailUserManager()


 