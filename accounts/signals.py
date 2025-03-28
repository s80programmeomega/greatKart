from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=UserProfile)
def generate_thumbnail(sender, instance: UserProfile, **kwargs):
    # Prevent recursion by checking if the thumbnail needs to be updated
    if instance.profile_picture:
        instance.generate_thumbnail()
        # Save the instance without triggering the signal again
        UserProfile.objects.filter(pk=instance.pk).update(thumbnail=instance.thumbnail)
    elif not instance.profile_picture and instance.thumbnail:
        instance.clear_thumbnail()
        # Save the instance without triggering the signal again
        UserProfile.objects.filter(pk=instance.pk).update(thumbnail=None)