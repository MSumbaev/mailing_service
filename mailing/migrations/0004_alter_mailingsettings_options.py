# Generated by Django 4.2.4 on 2023-10-02 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_client_owner_mailingmessage_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailingsettings',
            options={'permissions': [('set_status', 'Can change status of mailing')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
