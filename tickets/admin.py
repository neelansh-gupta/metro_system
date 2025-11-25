from django.contrib import admin
from .models import Ticket, TicketScan


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'user', 'origin', 'destination', 'price', 'status', 'purchased_at')
    list_filter = ('status', 'purchased_at')
    search_fields = ('ticket_id', 'user__username', 'origin__name', 'destination__name')
    readonly_fields = ('ticket_id', 'purchased_at')
    date_hierarchy = 'purchased_at'
    ordering = ('-purchased_at',)


@admin.register(TicketScan)
class TicketScanAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'station', 'scan_type', 'scanned_by', 'scanned_at', 'success')
    list_filter = ('scan_type', 'success', 'scanned_at')
    search_fields = ('ticket__ticket_id', 'station__name', 'scanned_by__username')
    date_hierarchy = 'scanned_at'
    ordering = ('-scanned_at',)
