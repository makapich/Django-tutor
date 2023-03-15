from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    command_help = 'Generates bulk users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, choices=range(1, 11), help='The number of users to generate')

    def handle(self, *args, **options):
        count = options['count']

        faker = Faker()
        users = []
        for i in range(count):
            username = faker.user_name()
            email = faker.ascii_email()
            password = faker.password()
            user = User(username=username, email=email, password=make_password(password))
            users.append(user)

        User.objects.bulk_create(users)

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {count} users!'))
