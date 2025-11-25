from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with additional fields for metro system."""
    
    USER_TYPE_CHOICES = [
        ('passenger', 'Passenger'),
        ('scanner', 'Ticket Scanner'),
        ('admin', 'Admin'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='passenger')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    @property
    def is_passenger(self):
        return self.user_type == 'passenger'
    
    @property
    def is_scanner(self):
        return self.user_type == 'scanner'
    
    @property
    def is_metro_admin(self):
        return self.user_type == 'admin'
    
    def add_balance(self, amount):
        """Add money to user's balance."""
        self.balance += amount
        self.save()
        return self.balance
    
    def deduct_balance(self, amount):
        """Deduct money from user's balance."""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False
