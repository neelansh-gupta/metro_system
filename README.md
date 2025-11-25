# 🚇 Metro Ticket System - Django Edition

A comprehensive Metro Ticket Purchasing System built with Django, PostgreSQL, Docker, and Nginx. This system enables passengers to purchase tickets, provides ticket scanning interfaces for verification, and includes an admin interface for managing metro lines and stations.

## 🔐 Google OAuth Setup (Optional)

To enable Google Login:

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select existing one
3. **Enable Google+ API**:
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API" and enable it
4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost/accounts/google/login/callback/`
     - `http://localhost:8000/accounts/google/login/callback/`
5. **Copy your credentials** and add to `.env` file:
   ```env
   GOOGLE_CLIENT_ID=your_client_id_here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_client_secret_here
   ```

## ✨ Features

### For Passengers
- 🎫 **Purchase Tickets**: Buy tickets between any two stations with automatic fare calculation
- 💰 **Wallet System**: Add money to account and manage balance
- 📱 **Ticket Management**: View active, used, and expired tickets
- 🗺️ **Route Planning**: Automatic shortest path calculation between stations
- 👤 **Profile Management**: Edit personal details and view transaction history

### For Ticket Scanners
- 📷 **Scan Tickets**: Verify tickets at entry and exit points
- 💵 **Offline Tickets**: Create tickets for cash payments
- 📊 **Scan History**: Track all scanning activities
- ✅ **Real-time Validation**: Instant ticket status verification

### For Administrators
- 🚊 **Metro Line Management**: Add/edit metro lines, control services
- 🏢 **Station Management**: Add new stations, mark interchanges
- 📈 **Footfall Reports**: Monitor daily passenger traffic at each station
- 🎮 **Service Control**: Start/stop metro services and enable/disable ticket booking
- 📊 **Analytics Dashboard**: View system-wide statistics and reports

## 🚀 Quick Start with Docker

### Option 1: Without Google Login
```bash
# Clone the repository
git clone <repository-url>
cd metro_ticket_system_task_1

# Start the entire system with one command
docker-compose up --build
```

### Option 2: With Google Login
```bash
# 1. Set up Google OAuth credentials (see below)
# 2. Create .env file with your credentials
cp env.example .env
# Edit .env and add your Google Client ID and Secret

# 3. Start with Google OAuth enabled
docker-compose up --build
```

That's it! The system will be available at:
- **Main Application**: http://localhost
- **Django Admin**: http://localhost/admin

## 🔑 Default Login Credentials

After running the system, use these credentials to log in:

| User Type | Username | Password | Description |
|-----------|----------|----------|-------------|
| Admin | admin | admin123 | Full system access |
| Scanner | scanner1 | scanner123 | Ticket scanning access |
| Passenger | passenger1 | pass123 | Regular passenger (Rs. 500 balance) |
| Passenger | passenger2 | pass123 | Regular passenger (Rs. 1000 balance) |

## 🏗️ System Architecture

### Technology Stack
- **Backend**: Django 4.2.7
- **Database**: PostgreSQL 15
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Containerization**: Docker & Docker Compose
- **Frontend**: Bootstrap 5 with custom styling

### Project Structure
```
metro_ticket_system_task_1/
├── accounts/           # User authentication and profiles
├── metro/             # Metro lines and stations management
├── tickets/           # Ticket purchasing and scanning
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── metro_system/      # Django project settings
├── docker-compose.yml # Docker orchestration
├── Dockerfile         # Container configuration
├── nginx.conf         # Nginx configuration
└── manage.py          # Django management script
```

## 📋 Features in Detail

### Phase 1 Implementation ✅

1. **Authentication System**
   - Custom user model with three types: Passengers, Scanners, Admins
   - Role-based access control
   - Session management

2. **Database Design**
   - PostgreSQL with Django ORM
   - Models for Users, Metro Lines, Stations, Tickets, Scans
   - Automatic fare calculation based on distance
   - Wallet system for passengers

3. **User Interfaces**
   - **Passengers**: Buy tickets, view history, manage profile, add balance
   - **Scanners**: Scan tickets, create offline tickets, view scan history
   - **Admins**: Manage lines/stations, view footfall, control services

4. **Ticket System**
   - Unique ticket IDs (UUID)
   - Status tracking: Active, In Use, Used, Expired
   - Automatic expiry after 24 hours
   - Path tracking for journey validation

5. **Admin Features**
   - Add/remove metro lines and stations
   - Monitor daily footfall at each station
   - Start/stop metro services per line
   - Enable/disable ticket booking per line

## 🛠️ Manual Installation (Without Docker)

If you prefer to run without Docker:

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- pip and virtualenv

### Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd metro_ticket_system_task_1
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up PostgreSQL**
```sql
CREATE DATABASE metro_db;
CREATE USER metro_user WITH PASSWORD 'metro_password';
GRANT ALL PRIVILEGES ON DATABASE metro_db TO metro_user;
```

5. **Configure environment**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=metro_db
DB_USER=metro_user
DB_PASSWORD=metro_password
DB_HOST=localhost
DB_PORT=5432
```

6. **Run migrations**
```bash
python manage.py migrate
```

7. **Initialize sample data**
```bash
python manage.py init_data
```

8. **Create static files**
```bash
python manage.py collectstatic
```

9. **Run the server**
```bash
python manage.py runserver
```

## 🎯 Usage Guide

### For Passengers

1. **Sign Up/Login**: Create an account as a passenger
2. **Add Balance**: Add money to your wallet (simulation)
3. **Purchase Ticket**: Select origin and destination stations
4. **View Tickets**: Check your active and past tickets
5. **Use Ticket**: Show ticket ID at station for scanning

### For Ticket Scanners

1. **Login**: Use scanner credentials
2. **Scan Entry**: Scan tickets when passengers enter
3. **Scan Exit**: Scan tickets when passengers exit
4. **Offline Tickets**: Create tickets for cash payments

### For Administrators

1. **Login**: Use admin credentials
2. **Manage Lines**: Add new metro lines or control existing ones
3. **Add Stations**: Create new stations on metro lines
4. **View Reports**: Monitor footfall and system statistics
5. **Control Services**: Start/stop lines and booking services

## 📊 Fare Calculation

- **Base Fare**: Rs. 10
- **Per Station**: Rs. 5
- **Formula**: Total Fare = Base Fare + (Number of Stations × Per Station Fare)

Example: Journey across 5 stations = Rs. 10 + (5 × Rs. 5) = Rs. 35

## 🚀 Deployment to DigitalOcean

### Quick Deploy

1. **Create a DigitalOcean Droplet**
   - Ubuntu 22.04 LTS
   - Minimum 2GB RAM
   - Open ports: 22 (SSH), 80 (HTTP), 443 (HTTPS)

2. **SSH into your droplet**
```bash
ssh root@your-droplet-ip
```

3. **Install Docker and Docker Compose**
```bash
apt update && apt upgrade -y
apt install docker.io docker-compose -y
```

4. **Clone and run**
```bash
git clone <repository-url>
cd metro_ticket_system_task_1

# Update ALLOWED_HOSTS in docker-compose.yml with your domain/IP
nano docker-compose.yml

# Run the application
docker-compose up -d
```

5. **Access your application**
   - Visit: http://your-droplet-ip

## 🔧 Configuration

### Environment Variables

All configuration is done through environment variables in `docker-compose.yml`:

- `SECRET_KEY`: Django secret key (change in production!)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Add your domain/IP
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`: Database credentials

### Nginx Configuration

The `nginx.conf` file handles:
- Static file serving
- Media file serving
- Proxy to Django application
- Client upload limits

## 📝 API Endpoints (Internal)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/login/` | GET/POST | User login |
| `/accounts/signup/` | GET/POST | User registration |
| `/accounts/profile/` | GET/POST | User profile |
| `/tickets/purchase/` | GET/POST | Purchase ticket |
| `/tickets/scan/` | POST | Scan ticket |
| `/metro/admin/` | GET | Admin dashboard |

## 🐛 Troubleshooting

### Common Issues

1. **Database connection error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`

2. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check Nginx configuration

3. **Docker issues**
   - Run `docker-compose down` then `docker-compose up --build`
   - Check logs: `docker-compose logs`

## 📚 Future Enhancements

- [ ] QR code generation for tickets
- [ ] Real payment gateway integration
- [ ] Mobile app development
- [ ] Real-time train tracking
- [ ] Multi-language support
- [ ] SMS/Email notifications
- [ ] Advanced analytics dashboard
- [ ] API for third-party integrations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For issues or questions, please create an issue in the repository or contact the development team.

---

**Made with ❤️ using Django and Docker**