# Generated by Django 5.1.3 on 2024-12-07 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_alter_livres_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Livres',
            new_name='Livre',
        ),
    ]