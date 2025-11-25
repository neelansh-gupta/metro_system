from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('purchase/', views.purchase_ticket, name='purchase'),
    path('my-tickets/', views.my_tickets, name='my_tickets'),
    path('ticket/<str:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('scanner/', views.scanner_dashboard, name='scanner_dashboard'),
    path('scan/', views.scan_ticket, name='scan_ticket'),
    path('scan-result/<str:ticket_id>/', views.scan_result, name='scan_result'),
    path('offline-ticket/', views.create_offline_ticket, name='create_offline_ticket'),
]
