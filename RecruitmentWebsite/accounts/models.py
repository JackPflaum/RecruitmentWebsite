from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

def use_directory_path(instance, filename):
    """returns the directory path where the media file will be stored"""
    # file will be uploaded to MEDIA_ROOT/user_id/filename
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def get_default_resume():
        """default resume used as placeholder before user adds their resume"""
        return settings.MEDIA_ROOT + '/default_resume.txt'
    

class Profile(models.Model):
    # extending User model using One-To-One link and signals in signals.py
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(default="default@email.com")
    phone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to=use_directory_path, default='images/default_profile_image.png', blank=True) # default='media/images/'
    resume = models.FileField(upload_to=use_directory_path, default=get_default_resume, blank=True)    # call function that returns file path.
    resume_last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username