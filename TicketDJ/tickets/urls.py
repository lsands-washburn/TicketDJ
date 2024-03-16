from django.urls import include, path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('mainapp/', include('mainapp.urls')),
    path('ticket-list/', views.ticket_list, name='ticket_list'),  # Choose a specific path for the ticket list view
]

