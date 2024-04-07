from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['issue_type', 'description', 'priority', 'assigned_to', 'ticket_status']
