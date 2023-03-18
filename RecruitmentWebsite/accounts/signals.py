from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


# sender: usually a model that notifies the receiver when an event occurs.
# receiver: usually a function that works on the data once it is notified when an action takes place.
# For instance when a user instance is about to be saved to the database.
# signal dispatcher: connects the sender and reciever.
# next step: connect the receivers in the ready() method of app's configuration apps.py

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """creates a Profile instance for the User that was created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """save Profile instance"""
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def deleting_old_resume(sender, instance, **kwargs):
    """delete old resume when submitting new resume"""
    if instance.pk:
        old_resume = Profile.objects.get(pk=instance.pk).resume
        new_resume = instance.resume
        if old_resume and old_resume.url != new_resume.url:
            old_resume.delete(save=False)