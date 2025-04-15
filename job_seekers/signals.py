from .models import CustomUser, Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



@receiver(post_save, sender=CustomUser)    
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile.objects.create(
            user=user
        )
        print('Profile created')

@receiver(post_delete, sender=CustomUser)        
def delete_profile(sender, instance, **kwargs):
    user = instance
    instance.profile.delete() 
    print('CustomUser associated with Profile has been deleted')