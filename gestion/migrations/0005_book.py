# Generated by Django 5.1.3 on 2024-12-07 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0004_rename_livres_livre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('auteur', models.CharField(max_length=100)),
                ('annee_publication', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='images')),
            ],
        ),
    ]
