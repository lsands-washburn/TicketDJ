from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('resolved', 'Resolved'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
    ]

    ISSUE_TYPE_CHOICES = [
        ('bug', 'Bug'),
        ('feature_request', 'Feature Request'),
        ('question', 'Question'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    ticket_id = models.AutoField(primary_key=True)
    issue_type = models.CharField(max_length=100, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tickets', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    created_datetime = models.DateTimeField(auto_now_add=True)
    closed_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    ticket_status = models.CharField(max_length=100, choices=TICKET_STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Ticket #{self.ticket_id}: {self.description}"
