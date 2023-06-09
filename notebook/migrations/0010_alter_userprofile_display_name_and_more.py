# Generated by Django 4.1.7 on 2023-03-28 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0009_alter_userprofile_display_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='display_name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
