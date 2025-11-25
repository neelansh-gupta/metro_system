from django import forms
from metro.models import Station


class TicketPurchaseForm(forms.Form):
    """Form for purchasing tickets."""
    
    origin = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True).select_related('line').order_by('line__name', 'position'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Station'
    )
    destination = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True).select_related('line').order_by('line__name', 'position'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='To Station'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin')
        destination = cleaned_data.get('destination')
        
        if origin and destination:
            if origin == destination:
                raise forms.ValidationError('Origin and destination cannot be the same.')
        
        return cleaned_data


class TicketScanForm(forms.Form):
    """Form for scanning tickets."""
    
    SCAN_TYPE_CHOICES = [
        ('entry', 'Entry'),
        ('exit', 'Exit'),
    ]
    
    ticket_id = forms.UUIDField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket ID'}),
        label='Ticket ID'
    )
    station = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Current Station'
    )
    scan_type = forms.ChoiceField(
        choices=SCAN_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Scan Type'
    )


class OfflineTicketForm(forms.Form):
    """Form for creating offline tickets."""
    
    passenger_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter passenger name'}),
        label='Passenger Name'
    )
    origin = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='From Station'
    )
    destination = forms.ModelChoiceField(
        queryset=Station.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='To Station'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get('origin')
        destination = cleaned_data.get('destination')
        
        if origin and destination:
            if origin == destination:
                raise forms.ValidationError('Origin and destination cannot be the same.')
        
        return cleaned_data
