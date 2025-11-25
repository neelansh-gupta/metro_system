# Metro Ticket System

Django-based metro ticket management system with Docker deployment.

## Quick Start

```bash
docker-compose up -d
```

Access the application at http://localhost

## Architecture

### Docker Compose Services

The `docker-compose.yml` file defines three services:

1. **db** - PostgreSQL 15 database
   - Stores all application data
   - Exposed on port 5432
   - Health checks ensure database is ready before starting web service

2. **web** - Django application
   - Runs database migrations on startup
   - Serves application on port 8000
   - Uses Gunicorn as WSGI server
   - Mounts local code for development

3. **nginx** - Reverse proxy
   - Handles incoming requests on port 80
   - Serves static files directly
   - Proxies dynamic requests to Django

### Nginx Configuration

The `nginx.conf` file configures:

- **Upstream server**: Points to Django application at web:8000
- **Static files**: Serves CSS/JS directly from /app/staticfiles
- **Media files**: Serves uploaded files from /app/media
- **Proxy settings**: Forwards requests to Django with proper headers
- **Client limits**: Max body size set to 10M for file uploads

## Default Credentials

- Admin: admin / admin123
- Scanner: scanner1 / scanner123
- Passenger: passenger1 / pass123

## Environment Variables

Key environment variables in docker-compose.yml:

- `SECRET_KEY`: Django secret key (change in production)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains
- `GOOGLE_CLIENT_ID`: OAuth client ID for Google login
- `GOOGLE_CLIENT_SECRET`: OAuth client secret

## Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Reset everything
docker-compose down -v
```
