from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.db import models
from datetime import datetime, timedelta
from collections import deque
from .models import MetroLine, Station, DailyFootfall
from .forms import MetroLineForm, StationForm
from tickets.models import Ticket


def is_admin(user):
    """Check if user is a metro admin."""
    return user.is_authenticated and user.is_metro_admin


@login_required
def dashboard(request):
    """Main dashboard that redirects based on user type."""
    if request.user.is_metro_admin:
        return redirect('metro:admin_dashboard')
    elif request.user.is_scanner:
        return redirect('tickets:scanner_dashboard')
    else:
        return redirect('metro:passenger_dashboard')


@login_required
def passenger_dashboard(request):
    """Dashboard for passengers."""
    active_tickets = Ticket.objects.filter(
        user=request.user,
        status__in=['active', 'in_use']
    ).order_by('-purchased_at')[:5]
    
    recent_tickets = Ticket.objects.filter(
        user=request.user
    ).order_by('-purchased_at')[:10]
    
    context = {
        'active_tickets': active_tickets,
        'recent_tickets': recent_tickets,
        'balance': request.user.balance,
    }
    return render(request, 'metro/passenger_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard for metro admins."""
    from tickets.models import Ticket
    lines = MetroLine.objects.all()
    stations = Station.objects.all()
    
    # Get today's date
    today = timezone.now().date()
    
    # Get today's footfall
    today_footfall = DailyFootfall.objects.filter(date=today).aggregate(
        total_entries=Sum('entry_count'),
        total_exits=Sum('exit_count')
    )
    
    # Get top stations by footfall
    top_stations = DailyFootfall.objects.filter(
        date=today
    ).annotate(
        total=models.F('entry_count') + models.F('exit_count')
    ).order_by('-total')[:5]
    
    # Get ticket statistics
    today_tickets = Ticket.objects.filter(purchased_at__date=today)
    total_tickets_today = today_tickets.count()
    total_revenue_today = today_tickets.aggregate(Sum('price'))['price__sum'] or 0
    
    # Get ticket status breakdown
    ticket_status = {
        'active': Ticket.objects.filter(status='active').count(),
        'in_use': Ticket.objects.filter(status='in_use').count(),
        'used': Ticket.objects.filter(status='used').count(),
        'expired': Ticket.objects.filter(status='expired').count(),
    }
    
    # Get recent tickets
    recent_tickets = Ticket.objects.select_related('user', 'origin', 'destination').order_by('-purchased_at')[:10]
    
    # Get station-wise ticket sales for today
    station_sales = today_tickets.values(
        'origin__name'
    ).annotate(
        count=Count('id'),
        revenue=Sum('price')
    ).order_by('-count')[:5]
    
    context = {
        'lines': lines,
        'stations': stations,
        'today_footfall': today_footfall,
        'top_stations': top_stations,
        'total_tickets_today': total_tickets_today,
        'total_revenue_today': total_revenue_today,
        'ticket_status': ticket_status,
        'recent_tickets': recent_tickets,
        'station_sales': station_sales,
    }
    return render(request, 'metro/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def manage_lines(request):
    """Manage metro lines."""
    lines = MetroLine.objects.all()
    
    if request.method == 'POST':
        form = MetroLineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Metro line added successfully!')
            return redirect('metro:manage_lines')
    else:
        form = MetroLineForm()
    
    context = {
        'lines': lines,
        'form': form,
    }
    return render(request, 'metro/manage_lines.html', context)


@login_required
@user_passes_test(is_admin)
def toggle_line_service(request, line_id):
    """Toggle metro line service status."""
    line = get_object_or_404(MetroLine, id=line_id)
    
    if line.is_active:
        line.end_service()
        messages.success(request, f'{line.name} Line service ended.')
    else:
        line.start_service()
        messages.success(request, f'{line.name} Line service started.')
    
    return redirect('metro:manage_lines')


@login_required
@user_passes_test(is_admin)
def toggle_line_booking(request, line_id):
    """Toggle ticket booking for a metro line."""
    line = get_object_or_404(MetroLine, id=line_id)
    
    if line.ticket_booking_enabled:
        line.disable_booking()
        messages.success(request, f'Ticket booking disabled for {line.name} Line.')
    else:
        line.enable_booking()
        messages.success(request, f'Ticket booking enabled for {line.name} Line.')
    
    return redirect('metro:manage_lines')


@login_required
@user_passes_test(is_admin)
def manage_stations(request):
    """Manage metro stations."""
    stations = Station.objects.all()
    
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Station added successfully!')
            return redirect('metro:manage_stations')
    else:
        form = StationForm()
    
    context = {
        'stations': stations,
        'form': form,
    }
    return render(request, 'metro/manage_stations.html', context)


@login_required
@user_passes_test(is_admin)
def footfall_report(request):
    """View footfall reports."""
    # Get date range from request or default to last 7 days
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=7)
    
    if request.GET.get('start_date'):
        start_date = datetime.strptime(request.GET['start_date'], '%Y-%m-%d').date()
    if request.GET.get('end_date'):
        end_date = datetime.strptime(request.GET['end_date'], '%Y-%m-%d').date()
    
    # Get footfall data
    footfall_data = DailyFootfall.objects.filter(
        date__range=[start_date, end_date]
    ).select_related('station').order_by('-date', 'station')
    
    # Aggregate data by station
    station_totals = footfall_data.values('station__name').annotate(
        total_entries=Sum('entry_count'),
        total_exits=Sum('exit_count'),
        total=Sum(models.F('entry_count') + models.F('exit_count'))
    ).order_by('-total')
    
    context = {
        'footfall_data': footfall_data,
        'station_totals': station_totals,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'metro/footfall_report.html', context)


def find_shortest_path(origin, destination):
    """Find shortest path between two stations using BFS, considering interchanges."""
    from metro.models import StationConnection
    
    if origin == destination:
        return [origin]
    
    # Build adjacency list including both line connections and interchanges
    adjacency = {}
    stations = Station.objects.filter(is_active=True).select_related('line')
    
    for station in stations:
        adjacency[station] = []
        
        # Add next and previous stations on the same line
        next_station = station.get_next_station()
        prev_station = station.get_previous_station()
        
        if next_station:
            adjacency[station].append(next_station)
        if prev_station:
            adjacency[station].append(prev_station)
        
        # Add interchange connections
        interchange_connections = StationConnection.objects.filter(
            from_station=station,
            connection_type='interchange'
        ).select_related('to_station')
        
        for connection in interchange_connections:
            if connection.to_station not in adjacency[station]:
                adjacency[station].append(connection.to_station)
    
    # BFS to find shortest path
    queue = deque([[origin]])
    visited = set()
    
    while queue:
        path = queue.popleft()
        current = path[-1]
        
        if current == destination:
            return path
        
        if current not in visited:
            visited.add(current)
            for neighbor in adjacency.get(current, []):
                if neighbor not in visited:
                    queue.append(path + [neighbor])
    
    return None


def calculate_fare(path):
    """Calculate fare based on path length."""
    from django.conf import settings
    if not path or len(path) < 2:
        return 0
    
    stations_crossed = len(path) - 1
    fare = settings.TICKET_BASE_FARE + (stations_crossed * settings.TICKET_PER_STATION_FARE)
    return fare
