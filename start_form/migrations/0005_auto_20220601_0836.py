# Generated by Django 3.0.8 on 2022-06-01 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_form', '0004_auto_20220531_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='voyage',
            name='date_heure_commande',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='voyage',
            name='date_heure_succces',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='voyage',
            name='date_heure_traitement',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
