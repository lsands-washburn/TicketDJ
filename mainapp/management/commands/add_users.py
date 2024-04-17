from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from faker import Faker
import pyodbc
from mainapp.views import db_connect

class Command(BaseCommand):
    help = 'Adds 70 users with pseudo-realistic information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        group_name = 'EndUser'  #desired group name
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Group {} does not exist'.format(group_name)))
            return
        conn = db_connect()
        cursor = conn.cursor()
        for _ in range(70):
            username = fake.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            password = 'password123'  #set a common password for all users
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.groups.add(group)  # Add user to the group
            cursor.execute("""INSERT INTO Helpdesk_User (username, email, first_name, last_name) VALUES (?, ?, ?, ?);""", [username, email, first_name, last_name])
            conn.commit()
        self.stdout.write(self.style.SUCCESS('Successfully added 70 users to group {}'.format(group_name)))
