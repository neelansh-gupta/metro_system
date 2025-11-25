from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import uuid
from metro.models import Station


class Ticket(models.Model):
    """Model for metro tickets."""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('in_use', 'In Use'),
        ('used', 'Used'),
        ('expired', 'Expired'),
    ]
    
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    origin = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='tickets_from')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='tickets_to')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    purchased_at = models.DateTimeField(auto_now_add=True)
    entry_time = models.DateTimeField(null=True, blank=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    path = models.JSONField(default=list, help_text="List of station IDs in the journey path")
    
    class Meta:
        ordering = ['-purchased_at']
    
    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.user.username}"
    
    @property
    def is_expired(self):
        """Check if ticket has expired."""
        expiry_time = self.purchased_at + timedelta(hours=settings.TICKET_EXPIRY_HOURS)
        return timezone.now() > expiry_time
    
    def check_and_update_expiry(self):
        """Check and update ticket expiry status."""
        if self.status == 'active' and self.is_expired:
            self.status = 'expired'
            self.save()
            return True
        return False
    
    def scan_entry(self, station):
        """Scan ticket at entry."""
        if self.status != 'active':
            return False, f"Ticket is {self.status}"
        
        if self.is_expired:
            self.status = 'expired'
            self.save()
            return False, "Ticket has expired"
        
        if station != self.origin:
            return False, f"Invalid entry station. Ticket is from {self.origin.name}"
        
        self.status = 'in_use'
        self.entry_time = timezone.now()
        self.save()
        
        # Update footfall
        from metro.models import DailyFootfall
        footfall, created = DailyFootfall.objects.get_or_create(
            station=station,
            date=timezone.now().date()
        )
        footfall.record_entry()
        
        return True, "Entry successful"
    
    def scan_exit(self, station):
        """Scan ticket at exit."""
        if self.status != 'in_use':
            return False, f"Ticket is {self.status}"
        
        if station != self.destination:
            return False, f"Invalid exit station. Ticket is to {self.destination.name}"
        
        self.status = 'used'
        self.exit_time = timezone.now()
        self.save()
        
        # Update footfall
        from metro.models import DailyFootfall
        footfall, created = DailyFootfall.objects.get_or_create(
            station=station,
            date=timezone.now().date()
        )
        footfall.record_exit()
        
        return True, "Exit successful"


class TicketScan(models.Model):
    """Model to track ticket scans."""
    
    SCAN_TYPE_CHOICES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='scans')
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='scans')
    scan_type = models.CharField(max_length=10, choices=SCAN_TYPE_CHOICES)
    scanned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    scanned_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    message = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-scanned_at']
    
    def __str__(self):
        return f"{self.scan_type} scan at {self.station} - {self.scanned_at}"
