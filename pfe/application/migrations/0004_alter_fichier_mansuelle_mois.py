# Generated by Django 5.0.3 on 2024-04-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_utilisateur_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='mois',
            field=models.CharField(max_length=20),
        ),
    ]
