from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='c_manager@skychimp.com',
            first_name='c_manager',
            last_name='c_manager',
            is_superuser=False,
            is_staff=True,
            is_active=True
        )

        user.set_password('c_manager')
        user.save()
