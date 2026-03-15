from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import random

class User(AbstractUser):
    ROLE_CHOICES = (
        ('RESTAURANT', 'Restaurant Donor'),
        ('INDIVIDUAL_DONOR', 'Individual Donor'),
        ('NGO_VOLUNTEER', 'NGO Volunteer'),
        ('INDIVIDUAL_VOLUNTEER', 'Individual Volunteer'),
    )

    role = models.CharField(max_length=25, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    
    # Role Specific Fields
    fssai_license = models.CharField(max_length=50, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    ngo_id = models.CharField(max_length=50, blank=True, null=True)
    
    # TIER 2: Set to True automatically during registration IF parent NGO is verified
    is_verified_ngo = models.BooleanField(default=False)

class NGO(models.Model):
    name = models.CharField(max_length=255)
    ngo_id = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    pincode = models.CharField(max_length=6)
    security_code = models.CharField(max_length=20)
    
    # TIER 1: Admin must manually check this in the admin portal
    is_verified = models.BooleanField(default=False, verbose_name="Verified by Admin")

    def __str__(self):
        status = "✅ Verified" if self.is_verified else "⏳ Pending Approval"
        return f"{self.name} - {self.ngo_id} ({status})"

class FoodListing(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Claimed', 'Claimed'),
        ('Verified', 'Verified'),
    )
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    food_name = models.CharField(max_length=200)
    quantity = models.IntegerField(help_text="Servings")
    image = models.ImageField(upload_to='food_images/')
    preservation_required = models.BooleanField(default=False)
    pincode = models.CharField(max_length=6)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claims')
    otp = models.CharField(max_length=6, blank=True, null=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

# Signal to notify volunteers when new food is listed
@receiver(post_save, sender=FoodListing)
def notify_volunteers(sender, instance, created, **kwargs):
    if created:
        # Notifications only go to NGO volunteers who belong to verified NGOs
        volunteers = User.objects.filter(
            role='NGO_VOLUNTEER',
            pincode=instance.pincode,
            is_verified_ngo=True
        ).values_list('email', flat=True)

        if volunteers:
            subject = f"🚨 New Food Alert in {instance.pincode}!"
            message = (
                f"Hi! {instance.food_name} is available (Serves {instance.quantity}).\n"
                f"Location: {instance.pincode}\n"
                f"Log in to ResQFood to claim it!"
            )
            send_mail(subject, message, 'notifications@resqfood.org', list(volunteers))