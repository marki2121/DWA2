# Generated by Django 3.2.6 on 2021-08-26 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profili', '0002_alter_account_managers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='slika_profila',
            new_name='profile_image',
        ),
    ]
