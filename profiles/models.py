from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """ A user profile model for maintaining default
    delivery information and order history
    """
    # OneToOneField is like a foreignKey but one profile for one user and one
    # user for one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=50, blank=True)
    default_phone_number = models.CharField(max_length=20, blank=True)
    default_street_address1 = models.CharField(max_length=80, blank=True)
    default_street_address2 = models.CharField(max_length=80, blank=True)
    default_town_or_city = models.CharField(max_length=40, blank=True)
    default_county = models.CharField(max_length=80, blank=True)
    default_postcode = models.CharField(max_length=20, blank=True)
    default_country = CountryField(blank_label='Country', null=True,
                                   blank=True)

    def __str__(self):
        return self.user.username


class AdminMessage(models.Model):
    """ An admin reply relating to a reference number
    """
    ref_number = models.CharField(max_length=32)
    admin_message = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-message_date"]

    def __str__(self):
        return self.message[:30]


class UserMessage(models.Model):
    """ A user message relating to a reference number
    """
    ref_number = models.CharField(max_length=32)
    user_message = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-message_date"]

    def __str__(self):
        return self.user_message[:30]


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """ Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
