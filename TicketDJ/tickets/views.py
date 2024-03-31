from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import pyodbc
from django.http import HttpResponseRedirect
import uuid
import datetime
from django.contrib import messages


@login_required
def dashboard(request):
    conn = db_connect()

    # Create cursor
    cursor = conn.cursor()

    # Execute query to fetch tickets
    if request.user.groups.filter(name='Technician').exists():
        cursor.execute("SELECT * FROM Ticket WHERE ASSIGNED_TO = ?", request.user.username)
    else:
        cursor.execute("SELECT * FROM Ticket WHERE CREATED_BY = ?", request.user.username)
    # Fetch all tickets
    tickets = cursor.fetchall()
    print('test')
    # Close cursor and connection
    cursor.close()
    conn.close()

    # Pass tickets to the template for rendering
    return render(request,'tickets/dashboard.html',{'section': 'dashboard', 'tickets': tickets})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        # Retrieve form data
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        created_by = request.user.username
        created_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ticket_id = "T" + str(uuid.uuid4())[:9]
        ticket_status = "Open"

        # Establish database connection
        conn = db_connect()
        cursor = conn.cursor()

        try:
            # Insert new ticket into the database
            cursor.execute("INSERT INTO Ticket (ticket_id, issue_type, description, priority, created_by, created_datetime, ticket_status) VALUES (?, ?, ?, ?, ?, ?, ?)", (ticket_id, issue_type, description, priority, created_by, created_datetime, ticket_status))

            # Commit changes
            conn.commit()
            cursor.close()
            conn.close()

            # Store ticket information in session
            request.session['ticket_info'] = {
                'ticket_id': ticket_id,
                'issue_type': issue_type,
                'description': description,
                'priority': priority
            }

            # Redirect to ticket created page
            return redirect('tickets:ticket_created')  # Adjust the URL name if needed
        except Exception as e:
            # Handle any database errors
            # Log the error
            print(f"Error creating ticket: {e}")
            # Set error message directly
            request.session['ticket_error'] = True
            return redirect('dashboard')  # Adjust the URL name if needed

    else:
        # If not a POST request, redirect to the dashboard
        return redirect('dashboard')  # Adjust the URL name if needed

@login_required
def ticket_created(request):
    ticket_info = request.session.pop('ticket_info', None)
    if ticket_info:
        return render(request, 'tickets/ticket_created.html', {'ticket_info': ticket_info})
    else:
        # Handle case where ticket information is not available
        return redirect('dashboard')  # or render an error page


@login_required
def ticket_list(request):
    # Database connection settings
    conn = db_connect()

    # Create cursor
    cursor = conn.cursor()

    # Execute query to fetch tickets
    if request.user.groups.filter(name='Technician').exists():
        cursor.execute("SELECT * FROM Ticket")
    else:
        cursor.execute("SELECT * FROM Ticket WHERE CREATED_BY = ?", request.user.username)
    # Fetch all tickets
    tickets = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Pass tickets to the template for rendering
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    conn = db_connect()
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
    # Establish database connection
    conn = db_connect()
    cursor = conn.cursor()

    note_text = request.POST.get('note')
    note_id = "N" + str(uuid.uuid4())[:9]
    created_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO Note (note_id, ticket_id, note, created_datetime, created_by) VALUES (?, ?, ?, ?, ?)", note_id, ticket_id, note_text, created_datetime, request.user.username)

    conn.commit()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def assign_ticket(request):
    conn = db_connect()
    cursor = conn.cursor()
    #get oldest ticket
    cursor.execute("""SELECT TOP 1 ticket_id 
                   FROM ticket
                   WHERE assigned_to IS NULL
                   ORDER BY created_datetime ASC;""")
    next_ticket = cursor.fetchone()
    next_ticket_id = next_ticket[0]
    cursor.close()
    conn.close()
    
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute("""UPDATE Ticket
                   SET assigned_to = (?)
                   WHERE ticket_id = (?);""", request.user.username, next_ticket_id)
    
    conn.commit()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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