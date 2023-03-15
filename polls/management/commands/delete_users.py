from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

User = get_user_model()


class Command(BaseCommand):
    command_help = 'Deletes users'

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int, help='User ids to delete')

    def handle(self, *args, **options):
        ids = options['ids']

        if User.objects.filter(pk__in=ids, is_superuser=True).exists():
            raise CommandError('Cannot delete superusers')

        users_to_delete_query = Q(pk__in=ids)
        num_deleted, _ = User.objects.filter(users_to_delete_query).delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {num_deleted} users with primary keys {ids}!'))
