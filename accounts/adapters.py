from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom adapter to set user type for social login users."""
    
    def populate_user(self, request, sociallogin, data):
        """Populate user instance with social account data."""
        user = super().populate_user(request, sociallogin, data)
        
        # Set default user type as passenger for Google login users
        user.user_type = 'passenger'
        
        # Set initial balance for new users
        user.balance = 100.00
        
        return user
    
    def save_user(self, request, sociallogin, form=None):
        """Save user with additional fields."""
        user = super().save_user(request, sociallogin, form)
        
        # Ensure user type and balance are set
        if not user.user_type:
            user.user_type = 'passenger'
        if not user.balance:
            user.balance = 100.00
        
        user.save()
        return user
