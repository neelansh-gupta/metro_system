from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class MetroLine(models.Model):
    """Model for metro lines."""
    
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20, default='blue')
    is_active = models.BooleanField(default=True)
    ticket_booking_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} Line"
    
    def start_service(self):
        """Start metro service for this line."""
        self.is_active = True
        self.save()
    
    def end_service(self):
        """End metro service for this line."""
        self.is_active = False
        self.save()
    
    def enable_booking(self):
        """Enable ticket booking for this line."""
        self.ticket_booking_enabled = True
        self.save()
    
    def disable_booking(self):
        """Disable ticket booking for this line."""
        self.ticket_booking_enabled = False
        self.save()


class Station(models.Model):
    """Model for metro stations."""
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    line = models.ForeignKey(MetroLine, on_delete=models.CASCADE, related_name='stations')
    position = models.IntegerField(help_text="Position of station on the line (for ordering)")
    is_interchange = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['line', 'position']
        unique_together = ['line', 'position']
    
    def __str__(self):
        return self.name  # Changed to just show name since we include line in name
    
    def clean(self):
        """Validate station data."""
        if self.position < 0:
            raise ValidationError("Position must be a positive integer.")
    
    def get_next_station(self):
        """Get the next station on the same line."""
        return Station.objects.filter(
            line=self.line,
            position=self.position + 1,
            is_active=True
        ).first()
    
    def get_previous_station(self):
        """Get the previous station on the same line."""
        return Station.objects.filter(
            line=self.line,
            position=self.position - 1,
            is_active=True
        ).first()


class StationConnection(models.Model):
    """Model for connections between stations (for interchanges)."""
    
    from_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='connections_from')
    to_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='connections_to')
    connection_type = models.CharField(
        max_length=20,
        choices=[
            ('normal', 'Normal'),
            ('interchange', 'Interchange'),
        ],
        default='normal'
    )
    
    class Meta:
        unique_together = ['from_station', 'to_station']
    
    def __str__(self):
        return f"{self.from_station} → {self.to_station}"
    
    def clean(self):
        """Validate connection."""
        if self.from_station == self.to_station:
            raise ValidationError("A station cannot connect to itself.")


class DailyFootfall(models.Model):
    """Model to track daily footfall at stations."""
    
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='footfall_records')
    date = models.DateField(default=timezone.now)
    entry_count = models.IntegerField(default=0)
    exit_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['station', 'date']
        ordering = ['-date', 'station']
    
    def __str__(self):
        return f"{self.station.name} - {self.date}: {self.total_footfall}"
    
    @property
    def total_footfall(self):
        """Calculate total footfall (entries + exits)."""
        return self.entry_count + self.exit_count
    
    def record_entry(self):
        """Record an entry at this station."""
        self.entry_count += 1
        self.save()
    
    def record_exit(self):
        """Record an exit at this station."""
        self.exit_count += 1
        self.save()
