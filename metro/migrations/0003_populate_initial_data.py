# Simple migration to populate initial metro data with multiple lines

from django.db import migrations


def populate_metro_data(apps, schema_editor):
    """Populate initial metro lines and stations with interchanges."""
    MetroLine = apps.get_model('metro', 'MetroLine')
    Station = apps.get_model('metro', 'Station')
    StationConnection = apps.get_model('metro', 'StationConnection')
    
    # Skip if data already exists
    if MetroLine.objects.exists():
        return
    
    # Create Blue Line
    blue_line = MetroLine.objects.create(
        name='Blue',
        color='#0000FF',
        is_active=True,
        ticket_booking_enabled=True
    )
    
    # Blue Line stations
    blue_stations = [
        ('Dwarka', 'DWK', 0, False),
        ('Janakpuri', 'JPK', 1, False),
        ('Rajouri Garden', 'RGD', 2, True),  # Interchange with Pink
        ('Karol Bagh', 'KBG', 3, False),
        ('Rajiv Chowk', 'RCK', 4, True),  # Interchange with Yellow
        ('Mandi House', 'MHS', 5, False),
        ('Pragati Maidan', 'PMD', 6, False),
        ('Akshardham', 'AKD', 7, False),
        ('Mayur Vihar', 'MVR', 8, False),
        ('Noida City Centre', 'NCC', 9, False),
    ]
    
    for name, code, position, is_interchange in blue_stations:
        Station.objects.create(
            name=f"{name} (Blue)",
            code=f"{code}_B",
            line=blue_line,
            position=position,
            is_interchange=is_interchange,
            is_active=True
        )
    
    # Create Yellow Line
    yellow_line = MetroLine.objects.create(
        name='Yellow',
        color='#FFD700',
        is_active=True,
        ticket_booking_enabled=True
    )
    
    # Yellow Line stations
    yellow_stations = [
        ('Samaypur Badli', 'SBD', 0, False),
        ('Rohini', 'RHN', 1, False),
        ('Pitampura', 'PTM', 2, False),
        ('Model Town', 'MTN', 3, False),
        ('Azadpur', 'AZP', 4, False),
        ('Rajiv Chowk', 'RCK', 5, True),  # Interchange with Blue
        ('Patel Chowk', 'PCK', 6, False),
        ('Central Secretariat', 'CST', 7, True),  # Interchange with Violet
        ('INA', 'INA', 8, False),
        ('AIIMS', 'AMS', 9, False),
        ('Green Park', 'GPK', 10, False),
        ('Hauz Khas', 'HKS', 11, True),  # Interchange with Magenta
        ('Malviya Nagar', 'MVN', 12, False),
        ('Saket', 'SKT', 13, False),
        ('Qutub Minar', 'QMR', 14, False),
        ('HUDA City Centre', 'HCC', 15, False),
    ]
    
    for name, code, position, is_interchange in yellow_stations:
        Station.objects.create(
            name=f"{name} (Yellow)",
            code=f"{code}_Y",
            line=yellow_line,
            position=position,
            is_interchange=is_interchange,
            is_active=True
        )
    
    # Create Pink Line
    pink_line = MetroLine.objects.create(
        name='Pink',
        color='#FFC0CB',
        is_active=True,
        ticket_booking_enabled=True
    )
    
    # Pink Line stations
    pink_stations = [
        ('Majlis Park', 'MPK', 0, False),
        ('Azadpur', 'AZP', 1, True),  # Interchange with Yellow
        ('Shalimar Bagh', 'SBG', 2, False),
        ('Netaji Subhash Place', 'NSP', 3, False),
        ('Punjabi Bagh', 'PBG', 4, False),
        ('Rajouri Garden', 'RGD', 5, True),  # Interchange with Blue
        ('Mayapuri', 'MYP', 6, False),
        ('Naraina', 'NRN', 7, False),
        ('Delhi Cantt', 'DCT', 8, False),
        ('Durgabai Deshmukh', 'DDD', 9, False),
        ('Sir Vishweshwaraiah', 'SVS', 10, False),
        ('Bhikaji Cama', 'BCM', 11, False),
        ('Sarojini Nagar', 'SJN', 12, False),
        ('INA', 'INA', 13, True),  # Interchange with Yellow
        ('South Extension', 'SEX', 14, False),
        ('Lajpat Nagar', 'LPN', 15, False),
    ]
    
    for name, code, position, is_interchange in pink_stations:
        Station.objects.create(
            name=f"{name} (Pink)",
            code=f"{code}_P",
            line=pink_line,
            position=position,
            is_interchange=is_interchange,
            is_active=True
        )
    
    # Create interchange connections
    # These represent the ability to change lines at interchange stations
    interchanges = [
        ('Rajiv Chowk (Blue)', 'Rajiv Chowk (Yellow)'),
        ('Rajouri Garden (Blue)', 'Rajouri Garden (Pink)'),
        ('Azadpur (Yellow)', 'Azadpur (Pink)'),
        ('INA (Yellow)', 'INA (Pink)'),
    ]
    
    for from_name, to_name in interchanges:
        from_station = Station.objects.get(name=from_name)
        to_station = Station.objects.get(name=to_name)
        
        # Create bidirectional connections
        StationConnection.objects.create(
            from_station=from_station,
            to_station=to_station,
            connection_type='interchange'
        )
        StationConnection.objects.create(
            from_station=to_station,
            to_station=from_station,
            connection_type='interchange'
        )


def populate_users(apps, schema_editor):
    """Populate initial users."""
    from django.contrib.auth.hashers import make_password
    User = apps.get_model('accounts', 'User')
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin',
            password=make_password('admin123'),
            email='admin@metro.com',
            user_type='admin',
            is_staff=True,
            is_superuser=True
        )
    
    # Create scanner user
    if not User.objects.filter(username='scanner1').exists():
        User.objects.create(
            username='scanner1',
            password=make_password('scanner123'),
            email='scanner@metro.com',
            user_type='scanner'
        )
    
    # Create passenger users
    if not User.objects.filter(username='passenger1').exists():
        User.objects.create(
            username='passenger1',
            password=make_password('pass123'),
            email='passenger1@example.com',
            user_type='passenger',
            balance=500.00
        )
    
    if not User.objects.filter(username='passenger2').exists():
        User.objects.create(
            username='passenger2',
            password=make_password('pass123'),
            email='passenger2@example.com',
            user_type='passenger',
            balance=1000.00
        )


def reverse_metro_data(apps, schema_editor):
    """Reverse migration - delete all data."""
    Station = apps.get_model('metro', 'Station')
    MetroLine = apps.get_model('metro', 'MetroLine')
    Station.objects.all().delete()
    MetroLine.objects.all().delete()


def reverse_users(apps, schema_editor):
    """Reverse migration - delete test users."""
    User = apps.get_model('accounts', 'User')
    User.objects.filter(username__in=['admin', 'scanner1', 'passenger1', 'passenger2']).delete()


def setup_site(apps, schema_editor):
    """Set up the default site for OAuth."""
    Site = apps.get_model('sites', 'Site')
    
    # Update or create the default site
    site, created = Site.objects.get_or_create(
        id=1,
        defaults={
            'domain': 'localhost',
            'name': 'Metro Ticket System'
        }
    )
    if not created:
        site.domain = 'localhost'
        site.name = 'Metro Ticket System'
        site.save()


def reverse_site(apps, schema_editor):
    """Reverse site setup."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('metro', '0002_initial'),
        ('accounts', '0002_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(populate_metro_data, reverse_metro_data),
        migrations.RunPython(populate_users, reverse_users),
        migrations.RunPython(setup_site, reverse_site),
    ]
