#!/usr/bin/env python
"""
Script to set up Google OAuth in the database.
Run this after migrations: python setup_google_oauth.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metro_system.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_oauth():
    """Set up Google OAuth app in database."""
    
    # Update site domain
    site = Site.objects.get_or_create(id=1)[0]
    site.domain = 'localhost'
    site.name = 'Metro Ticket System'
    site.save()
    print(f'✅ Site configured: {site.domain}')
    
    # Get Google credentials from environment
    client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    
    if not client_id or not client_secret:
        print('⚠️  Warning: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set in environment')
        print('   Google login will not work without these credentials')
        return
    
    # Create or update Google OAuth app
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Google',
            'client_id': client_id,
            'secret': client_secret
        }
    )
    
    if not created:
        # Update existing app
        google_app.client_id = client_id
        google_app.secret = client_secret
        google_app.save()
        print('✅ Google OAuth app updated')
    else:
        print('✅ Google OAuth app created')
    
    # Add site to the app
    if site not in google_app.sites.all():
        google_app.sites.add(site)
        print('✅ Site added to Google OAuth app')
    
    print(f'\n📝 Google OAuth Configuration:')
    print(f'   Client ID: {client_id[:20]}...')
    print(f'   Redirect URI: http://localhost/accounts/google/login/callback/')
    print(f'\n⚠️  Make sure this redirect URI is added in your Google Cloud Console!')

if __name__ == '__main__':
    setup_google_oauth()
