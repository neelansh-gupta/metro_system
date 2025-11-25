from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form."""
    
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES, initial='passenger')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'user_type', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AddBalanceForm(forms.Form):
    """Form for adding balance to user account."""
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=10,
        max_value=10000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount (min: Rs. 10)'})
    )
