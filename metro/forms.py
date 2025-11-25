from django import forms
from .models import MetroLine, Station


class MetroLineForm(forms.ModelForm):
    """Form for creating/editing metro lines."""
    
    class Meta:
        model = MetroLine
        fields = ['name', 'color', 'is_active', 'ticket_booking_enabled']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ticket_booking_enabled': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class StationForm(forms.ModelForm):
    """Form for creating/editing stations."""
    
    class Meta:
        model = Station
        fields = ['name', 'code', 'line', 'position', 'is_interchange', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'line': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'is_interchange': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
