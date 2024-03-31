from django.urls import include, path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('mainapp/', include('mainapp.urls')),
    path('ticket-list/', views.ticket_list, name='ticket_list'),
    path('ticket/<ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('add_note/<ticket_id>/', views.add_note, name='add_note'),  
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('ticket_created/', views.ticket_created, name='ticket_created'),
]

