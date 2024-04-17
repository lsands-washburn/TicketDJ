from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Adds 70 users with pseudo-realistic information'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(70):
            username = fake.user_name()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email()
            password = 'password123'  #common password for all users
            User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        self.stdout.write(self.style.SUCCESS('Successfully added 70 users'))
