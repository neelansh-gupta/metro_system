from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, AddBalanceForm
from .models import User


class SignUpView(CreateView):
    """User registration view."""
    
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please login.')
        return response


def login_view(request):
    """Custom login view."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on user type
            if user.is_metro_admin:
                return redirect('metro:admin_dashboard')
            elif user.is_scanner:
                return redirect('tickets:scanner_dashboard')
            else:
                return redirect('metro:passenger_dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """User profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def add_balance_view(request):
    """Add balance to user account."""
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.add_balance(amount)
            messages.success(request, f'Rs. {amount} added to your account successfully!')
            return redirect('accounts:profile')
    else:
        form = AddBalanceForm()
    
    return render(request, 'accounts/add_balance.html', {'form': form})
