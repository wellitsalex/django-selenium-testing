# Generated by Django 4.1.7 on 2023-03-23 00:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0002_alter_user_email_address_alter_user_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
