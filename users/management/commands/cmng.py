from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='manager@skychimp.com',
            first_name='manager',
            last_name='manager',
            is_superuser=False,
            is_staff=True,
            is_active=True
        )

        user.set_password('manager')
        user.save()
