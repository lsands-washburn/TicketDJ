from django.urls import include, path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('mainapp/', include('mainapp.urls')),
    path('ticket-list/', views.ticket_list, name='ticket_list'),
    path('ticket/<ticket_id>/', views.ticket_detail, name='ticket_detail'),  # Choose a specific path for the ticket list view
]

