from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pyodbc

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
    cursor.execute("SELECT * FROM Ticket")

    # Fetch all tickets
    tickets = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Pass tickets to the template for rendering
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})
