from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=6, blank=True, null=True)
    email_verification_token_created = models.DateTimeField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def generate_email_verification_token(self):
        """Generate a 6-digit OTP for email verification"""
        self.email_verification_token = ''.join(random.choices(string.digits, k=6))
        self.email_verification_token_created = timezone.now()
        self.save()
        return self.email_verification_token
    
    def is_email_verification_token_valid(self):
        """Check if the email verification token is still valid (10 minutes)"""
        if not self.email_verification_token_created:
            return False
        return timezone.now() - self.email_verification_token_created < timezone.timedelta(minutes=10)
    
    def verify_email_token(self, token):
        """Verify the email token and mark email as verified"""
        if self.email_verification_token == token and self.is_email_verification_token_valid():
            self.is_email_verified = True
            self.email_verification_token = None
            self.email_verification_token_created = None
            self.save()
            return True
        return False
