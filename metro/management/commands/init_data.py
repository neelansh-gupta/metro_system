from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import User
from metro.models import MetroLine, Station


class Command(BaseCommand):
    help = 'Initialize the database with sample metro data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Initializing metro system data...')
        
        with transaction.atomic():
            # Create sample users
            self.create_users()
            
            # Create metro lines and stations
            self.create_metro_lines()
            
        self.stdout.write(self.style.SUCCESS('Successfully initialized metro system data!'))
    
    def create_users(self):
        """Create sample users for testing."""
        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_user(
                username='admin',
                password='admin123',
                email='admin@metro.com',
                user_type='admin',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(f'Created admin user: admin (password: admin123)')
        
        # Create scanner user
        if not User.objects.filter(username='scanner1').exists():
            scanner_user = User.objects.create_user(
                username='scanner1',
                password='scanner123',
                email='scanner@metro.com',
                user_type='scanner'
            )
            self.stdout.write(f'Created scanner user: scanner1 (password: scanner123)')
        
        # Create passenger users
        if not User.objects.filter(username='passenger1').exists():
            passenger1 = User.objects.create_user(
                username='passenger1',
                password='pass123',
                email='passenger1@example.com',
                user_type='passenger',
                balance=500.00
            )
            self.stdout.write(f'Created passenger user: passenger1 (password: pass123)')
        
        if not User.objects.filter(username='passenger2').exists():
            passenger2 = User.objects.create_user(
                username='passenger2',
                password='pass123',
                email='passenger2@example.com',
                user_type='passenger',
                balance=1000.00
            )
            self.stdout.write(f'Created passenger user: passenger2 (password: pass123)')
    
    def create_metro_lines(self):
        """Create metro lines and stations."""
        # Check if data already exists
        if MetroLine.objects.exists():
            self.stdout.write('Metro lines already exist, skipping...')
            return
        
        # Create Red Line
        red_line = MetroLine.objects.create(
            name='Red',
            color='#FF0000',
            is_active=True,
            ticket_booking_enabled=True
        )
        
        red_stations = [
            ('Rithala', 'RTL', 0),
            ('Rohini West', 'RHW', 1),
            ('Rohini East', 'RHE', 2),
            ('Pitampura', 'PTM', 3),
            ('Kohat Enclave', 'KHE', 4),
            ('Netaji Subhash Place', 'NSP', 5),
            ('Keshav Puram', 'KPM', 6),
            ('Kanhaiya Nagar', 'KNR', 7),
            ('Inderlok', 'ILK', 8),
            ('Shastri Nagar', 'STN', 9),
            ('Pratap Nagar', 'PTN', 10),
            ('Pulbangash', 'PBG', 11),
            ('Tis Hazari', 'THZ', 12),
            ('Kashmere Gate', 'KGT', 13),
            ('Shastri Park', 'STP', 14),
            ('Seelampur', 'SLP', 15),
            ('Welcome', 'WLC', 16),
            ('Shahdara', 'SHD', 17),
            ('Mansarovar Park', 'MPK', 18),
            ('Jhilmil', 'JML', 19),
            ('Dilshad Garden', 'DGN', 20),
        ]
        
        for name, code, position in red_stations:
            Station.objects.create(
                name=name,
                code=code,
                line=red_line,
                position=position,
                is_interchange=(name == 'Kashmere Gate'),
                is_active=True
            )
        
        self.stdout.write(f'Created Red Line with {len(red_stations)} stations')
        
        # Create Blue Line
        blue_line = MetroLine.objects.create(
            name='Blue',
            color='#0000FF',
            is_active=True,
            ticket_booking_enabled=True
        )
        
        blue_stations = [
            ('Dwarka Sector 21', 'DS21', 0),
            ('Dwarka Sector 8', 'DS8', 1),
            ('Dwarka Sector 9', 'DS9', 2),
            ('Dwarka Sector 10', 'DS10', 3),
            ('Dwarka Sector 11', 'DS11', 4),
            ('Dwarka Sector 12', 'DS12', 5),
            ('Dwarka Sector 13', 'DS13', 6),
            ('Dwarka Sector 14', 'DS14', 7),
            ('Dwarka', 'DWK', 8),
            ('Dwarka Mor', 'DWM', 9),
            ('Nawada', 'NWD', 10),
            ('Uttam Nagar West', 'UNW', 11),
            ('Uttam Nagar East', 'UNE', 12),
            ('Janakpuri West', 'JPW', 13),
            ('Janakpuri East', 'JPE', 14),
            ('Tilak Nagar', 'TNG', 15),
            ('Subhash Nagar', 'SNG', 16),
            ('Tagore Garden', 'TGN', 17),
            ('Rajouri Garden', 'RGN', 18),
            ('Ramesh Nagar', 'RNG', 19),
            ('Moti Nagar', 'MNG', 20),
            ('Kirti Nagar', 'KTN', 21),
            ('Shadipur', 'SDP', 22),
            ('Patel Nagar', 'PNG', 23),
            ('Rajendra Place', 'RPL', 24),
            ('Karol Bagh', 'KBG', 25),
            ('Jhandewalan', 'JDW', 26),
            ('RK Ashram Marg', 'RAM', 27),
            ('Rajiv Chowk', 'RCK', 28),
            ('Barakhamba', 'BKB', 29),
            ('Mandi House', 'MHS', 30),
            ('Pragati Maidan', 'PMN', 31),
            ('Indraprastha', 'IPS', 32),
            ('Yamuna Bank', 'YBK', 33),
            ('Akshardham', 'AKD', 34),
            ('Mayur Vihar 1', 'MV1', 35),
            ('Mayur Vihar Extension', 'MVE', 36),
            ('New Ashok Nagar', 'NAN', 37),
            ('Noida Sector 15', 'NS15', 38),
            ('Noida Sector 16', 'NS16', 39),
            ('Noida Sector 18', 'NS18', 40),
            ('Botanical Garden', 'BTG', 41),
            ('Golf Course', 'GFC', 42),
            ('Noida City Centre', 'NCC', 43),
            ('Sector 34', 'S34', 44),
            ('Sector 52', 'S52', 45),
            ('Sector 61', 'S61', 46),
            ('Sector 59', 'S59', 47),
            ('Sector 62', 'S62', 48),
            ('Noida Electronic City', 'NEC', 49),
        ]
        
        for name, code, position in blue_stations:
            Station.objects.create(
                name=name,
                code=code,
                line=blue_line,
                position=position,
                is_interchange=(name in ['Rajiv Chowk', 'Botanical Garden']),
                is_active=True
            )
        
        self.stdout.write(f'Created Blue Line with {len(blue_stations)} stations')
        
        # Create Yellow Line
        yellow_line = MetroLine.objects.create(
            name='Yellow',
            color='#FFFF00',
            is_active=True,
            ticket_booking_enabled=True
        )
        
        yellow_stations = [
            ('Samaypur Badli', 'SBD', 0),
            ('Rohini Sector 18', 'RS18', 1),
            ('Haiderpur Badli Mor', 'HBM', 2),
            ('Jahangirpuri', 'JGP', 3),
            ('Adarsh Nagar', 'ADN', 4),
            ('Azadpur', 'AZP', 5),
            ('Model Town', 'MTN', 6),
            ('GTB Nagar', 'GTB', 7),
            ('Vishwavidyalaya', 'VVD', 8),
            ('Vidhan Sabha', 'VSB', 9),
            ('Civil Lines', 'CVL', 10),
            ('Kashmere Gate', 'KGT', 11),
            ('Chandni Chowk', 'CCK', 12),
            ('Chawri Bazar', 'CBZ', 13),
            ('New Delhi', 'NDL', 14),
            ('Rajiv Chowk', 'RCK', 15),
            ('Patel Chowk', 'PCK', 16),
            ('Central Secretariat', 'CST', 17),
            ('Udyog Bhawan', 'UBN', 18),
            ('Race Course', 'RCS', 19),
            ('Jor Bagh', 'JBG', 20),
            ('INA', 'INA', 21),
            ('AIIMS', 'AMS', 22),
            ('Green Park', 'GPK', 23),
            ('Hauz Khas', 'HKS', 24),
            ('Malviya Nagar', 'MVN', 25),
            ('Saket', 'SKT', 26),
            ('Qutab Minar', 'QMR', 27),
            ('Chhattarpur', 'CTP', 28),
            ('Sultanpur', 'STP', 29),
            ('Ghitorni', 'GTN', 30),
            ('Arjan Garh', 'AGH', 31),
            ('Guru Dronacharya', 'GDC', 32),
            ('Sikanderpur', 'SKP', 33),
            ('MG Road', 'MGR', 34),
            ('IFFCO Chowk', 'IFC', 35),
            ('HUDA City Centre', 'HCC', 36),
        ]
        
        for name, code, position in yellow_stations:
            Station.objects.create(
                name=name,
                code=code,
                line=yellow_line,
                position=position,
                is_interchange=(name in ['Kashmere Gate', 'Rajiv Chowk', 'Hauz Khas']),
                is_active=True
            )
        
        self.stdout.write(f'Created Yellow Line with {len(yellow_stations)} stations')
