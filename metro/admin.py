from django.contrib import admin
from .models import MetroLine, Station, StationConnection, DailyFootfall


@admin.register(MetroLine)
class MetroLineAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'is_active', 'ticket_booking_enabled', 'created_at')
    list_filter = ('is_active', 'ticket_booking_enabled')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'line', 'position', 'is_interchange', 'is_active')
    list_filter = ('line', 'is_interchange', 'is_active')
    search_fields = ('name', 'code')
    ordering = ('line', 'position')


@admin.register(StationConnection)
class StationConnectionAdmin(admin.ModelAdmin):
    list_display = ('from_station', 'to_station', 'connection_type')
    list_filter = ('connection_type',)
    search_fields = ('from_station__name', 'to_station__name')


@admin.register(DailyFootfall)
class DailyFootfallAdmin(admin.ModelAdmin):
    list_display = ('station', 'date', 'entry_count', 'exit_count', 'total_footfall')
    list_filter = ('date', 'station')
    search_fields = ('station__name',)
    date_hierarchy = 'date'
    ordering = ('-date', 'station')
