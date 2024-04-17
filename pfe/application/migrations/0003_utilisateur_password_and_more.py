# Generated by Django 5.0.3 on 2024-04-17 19:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_alter_fichier_mansuelle_apport_consommation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='password',
            field=models.CharField(default='SONATRACH12', max_length=128, validators=[django.core.validators.RegexValidator(message='Le mot de passe doit contenir au moins 8 caractères avec des lettres et des chiffres.', regex='^(?=.*\\d)(?=.*[a-zA-Z]).{8,}$')]),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='Apport_consommation',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='consomme',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='densite',
            field=models.DecimalField(decimal_places=1, max_digits=3),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='expedie',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='laivraison',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='pertes',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='preleve',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='produit',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='fichier_mansuelle',
            name='stock_ini',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
