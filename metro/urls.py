from django.urls import path
from . import views

app_name = 'metro'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('passenger/', views.passenger_dashboard, name='passenger_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/lines/', views.manage_lines, name='manage_lines'),
    path('admin/lines/<int:line_id>/toggle-service/', views.toggle_line_service, name='toggle_line_service'),
    path('admin/lines/<int:line_id>/toggle-booking/', views.toggle_line_booking, name='toggle_line_booking'),
    path('admin/stations/', views.manage_stations, name='manage_stations'),
    path('admin/footfall/', views.footfall_report, name='footfall_report'),
]
