from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import transaction, models
from django.utils import timezone
from django.db.models import Q, Case, When
from .models import Ticket, TicketScan
from .forms import TicketPurchaseForm, TicketScanForm, OfflineTicketForm
from metro.models import Station
from metro.views import find_shortest_path, calculate_fare


def is_scanner(user):
    """Check if user is a ticket scanner."""
    return user.is_authenticated and (user.is_scanner or user.is_metro_admin)


@login_required
def purchase_ticket(request):
    """Purchase a new ticket."""
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            
            # Check if line is active and booking enabled
            if not origin.line.is_active or not origin.line.ticket_booking_enabled:
                messages.error(request, f'{origin.line.name} Line is not available for booking.')
                return redirect('tickets:purchase')
            
            # Find path and calculate fare
            path = find_shortest_path(origin, destination)
            if not path:
                messages.error(request, 'No route available between selected stations.')
                return redirect('tickets:purchase')
            
            fare = calculate_fare(path)
            
            # Check user balance
            if request.user.balance < fare:
                messages.error(request, f'Insufficient balance. Required: Rs. {fare}, Available: Rs. {request.user.balance}')
                return redirect('accounts:add_balance')
            
            # Create ticket and deduct balance
            with transaction.atomic():
                ticket = Ticket.objects.create(
                    user=request.user,
                    origin=origin,
                    destination=destination,
                    price=fare,
                    path=[s.id for s in path]
                )
                request.user.deduct_balance(fare)
            
            messages.success(request, f'Ticket purchased successfully! Ticket ID: {ticket.ticket_id}')
            return redirect('tickets:ticket_detail', ticket_id=str(ticket.ticket_id))
    else:
        form = TicketPurchaseForm()
    
    context = {
        'form': form,
        'balance': request.user.balance,
    }
    return render(request, 'tickets/purchase.html', context)


@login_required
def my_tickets(request):
    """View user's tickets."""
    # Update expired tickets
    active_tickets = Ticket.objects.filter(user=request.user, status='active')
    for ticket in active_tickets:
        ticket.check_and_update_expiry()
    
    tickets = Ticket.objects.filter(user=request.user).order_by('-purchased_at')
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'tickets/my_tickets.html', context)


@login_required
def ticket_detail(request, ticket_id):
    """View ticket details."""
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    
    # Check if user owns the ticket or is staff
    if ticket.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this ticket.')
        return redirect('tickets:my_tickets')
    
    # Check and update expiry
    ticket.check_and_update_expiry()
    
    # Get path stations
    path_stations = []
    if ticket.path:
        path_stations = Station.objects.filter(id__in=ticket.path).order_by(
            models.Case(*[models.When(id=pk, then=pos) for pos, pk in enumerate(ticket.path)])
        )
    
    context = {
        'ticket': ticket,
        'path_stations': path_stations,
    }
    return render(request, 'tickets/ticket_detail.html', context)


@login_required
@user_passes_test(is_scanner)
def scanner_dashboard(request):
    """Dashboard for ticket scanners."""
    recent_scans = TicketScan.objects.filter(
        scanned_by=request.user
    ).order_by('-scanned_at')[:10]
    
    today = timezone.now().date()
    today_scans = TicketScan.objects.filter(
        scanned_by=request.user,
        scanned_at__date=today
    ).count()
    
    context = {
        'recent_scans': recent_scans,
        'today_scans': today_scans,
    }
    return render(request, 'tickets/scanner_dashboard.html', context)


@login_required
@user_passes_test(is_scanner)
def scan_ticket(request):
    """Scan a ticket."""
    if request.method == 'POST':
        form = TicketScanForm(request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            station = form.cleaned_data['station']
            scan_type = form.cleaned_data['scan_type']
            
            try:
                ticket = Ticket.objects.get(ticket_id=ticket_id)
            except Ticket.DoesNotExist:
                messages.error(request, 'Invalid ticket ID.')
                return redirect('tickets:scan_ticket')
            
            # Perform scan based on type
            if scan_type == 'entry':
                success, message = ticket.scan_entry(station)
            else:
                success, message = ticket.scan_exit(station)
            
            # Record scan
            TicketScan.objects.create(
                ticket=ticket,
                station=station,
                scan_type=scan_type,
                scanned_by=request.user,
                success=success,
                message=message
            )
            
            if success:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('tickets:scan_result', ticket_id=str(ticket.ticket_id))
    else:
        form = TicketScanForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tickets/scan_ticket.html', context)


@login_required
@user_passes_test(is_scanner)
def scan_result(request, ticket_id):
    """Show scan result."""
    ticket = get_object_or_404(Ticket, ticket_id=ticket_id)
    last_scan = ticket.scans.first()
    
    context = {
        'ticket': ticket,
        'last_scan': last_scan,
    }
    return render(request, 'tickets/scan_result.html', context)


@login_required
@user_passes_test(is_scanner)
def create_offline_ticket(request):
    """Create ticket for offline payment."""
    if request.method == 'POST':
        form = OfflineTicketForm(request.POST)
        if form.is_valid():
            origin = form.cleaned_data['origin']
            destination = form.cleaned_data['destination']
            passenger_name = form.cleaned_data['passenger_name']
            
            # Find path and calculate fare
            path = find_shortest_path(origin, destination)
            if not path:
                messages.error(request, 'No route available between selected stations.')
                return redirect('tickets:create_offline_ticket')
            
            fare = calculate_fare(path)
            
            # Create or get offline user
            from accounts.models import User
            offline_user, created = User.objects.get_or_create(
                username=f'offline_{passenger_name.lower().replace(" ", "_")}',
                defaults={
                    'first_name': passenger_name,
                    'user_type': 'passenger',
                }
            )
            
            # Create ticket
            with transaction.atomic():
                ticket = Ticket.objects.create(
                    user=offline_user,
                    origin=origin,
                    destination=destination,
                    price=fare,
                    path=[s.id for s in path],
                    status='used'  # Mark as used immediately
                )
                
                # Record entry and exit scans
                TicketScan.objects.create(
                    ticket=ticket,
                    station=origin,
                    scan_type='entry',
                    scanned_by=request.user,
                    success=True,
                    message='Offline ticket - Entry recorded'
                )
                
                TicketScan.objects.create(
                    ticket=ticket,
                    station=destination,
                    scan_type='exit',
                    scanned_by=request.user,
                    success=True,
                    message='Offline ticket - Exit recorded'
                )
            
            messages.success(request, f'Offline ticket created. Fare: Rs. {fare}')
            return redirect('tickets:ticket_detail', ticket_id=str(ticket.ticket_id))
    else:
        form = OfflineTicketForm()
    
    context = {
        'form': form,
    }
    return render(request, 'tickets/create_offline_ticket.html', context)
