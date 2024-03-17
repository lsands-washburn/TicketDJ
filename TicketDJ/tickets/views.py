from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pyodbc
from django.http import HttpResponseRedirect
import uuid

@login_required
def ticket_list(request):
    # Database connection settings
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

    # Create cursor
    cursor = conn.cursor()

    # Execute query to fetch tickets
    if request.user.groups.filter(name='Technician').exists():
        cursor.execute("SELECT * FROM Ticket")
    else:
        cursor.execute("SELECT * FROM Ticket WHERE CREATED_BY = ?", request.user.id)
    # Fetch all tickets
    tickets = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Pass tickets to the template for rendering
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
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
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Ticket WHERE Ticket_Id = ?", ticket_id)
    ticket = cursor.fetchone()

    cursor.execute("SELECT * FROM Note WHERE Ticket_Id = ?", ticket_id)
    notes = cursor.fetchall()

    cursor.close()
    conn.close()
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'notes': notes})

@login_required
def add_note(request, ticket_id):
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
    cursor = conn.cursor()

    note_text = request.POST.get('note')
    note_id = "N" + str(uuid.uuid4())[:9]
    cursor.execute("INSERT INTO Note (note_id, note, ticket_id) VALUES (?, ?, ?)", note_id, note_text, ticket_id)

    conn.commit()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


