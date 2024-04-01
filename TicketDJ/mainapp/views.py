from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import pyodbc

from .forms import *

# Create your views here.

@login_required
def dashboard(request):
    #get tickets for the 
    conn = db_connect()
    cursor = conn.cursor()
    if request.user.groups.filter(name='Technician').exists():
        cursor.execute("SELECT * FROM Ticket WHERE ASSIGNED_TO = ?", request.user.username)
    else:
        cursor.execute("SELECT * FROM Ticket WHERE CREATED_BY = ?", request.user.username)
    tickets = cursor.fetchall()
    cursor.close()
    conn.close()

    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""select q.issue_type, queue_total, oldest_ticket 
                   from (select issue_type, count(distinct ticket_id) as queue_total from Ticket group by issue_type) q 
                   join (select issue_type, min(created_datetime) as oldest_ticket from Ticket group by issue_type) o 
                   on q.issue_type = o.issue_type order by queue_total desc""")
    queue_status = cursor.fetchall()
    cursor.close()
    conn.close()

    # Pass tickets to the template for rendering
    return render(request,'tickets/dashboard.html',{'section': 'dashboard', 'tickets': tickets, 'queue_status': queue_status})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #Create new user object 
            new_user = user_form.save(commit=False)
            #set passwd
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            
            #include code to set group
            user_group = Group.objects.get(name='EndUser')
            new_user.groups.add(user_group)

            #add user to sqlserver db
            conn = db_connect()
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO Helpdesk_User (username, email, first_name, last_name) VALUES (?, ?, ?, ?);""", [new_user.username, new_user.email, new_user.first_name, new_user.last_name])
            conn.commit()

            return render(request, 'registration/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

def db_connect():
    db_settings = {
        'driver': '{ODBC Driver 17 for SQL Server}',
        'server': 'cm465.database.windows.net',
        'database': 'HelpdeskProject',
        'user': 'CM465Admin@cm465',
        'password': 'CM465Password!',
    }

    # Establish database connection
    conn = pyodbc.connect(
        f"DRIVER={db_settings['driver']};SERVER={db_settings['server']};DATABASE={db_settings['database']};UID={db_settings['user']};PWD={db_settings['password']}"
    )
    return conn