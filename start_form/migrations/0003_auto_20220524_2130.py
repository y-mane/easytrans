# Generated by Django 3.0.8 on 2022-05-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_form', '0002_auto_20220523_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voyage',
            name='statut_commande',
            field=models.CharField(blank=True, choices=[('validée', 'validée'), ('échouée', 'échouée'), ('en attente', 'en attente')], default='en attente', max_length=250),
        ),
    ]
