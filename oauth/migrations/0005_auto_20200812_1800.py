# Generated by Django 3.0.8 on 2020-08-12 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_auto_20200812_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userboardpermission',
            options={'permissions': (('view_dashboard', 'Peut visualiser le Tableau de Bord'), ('send_short_messages', 'Peut Envoyer des SMS'), ('send_mail', 'Peut envoyer des eMails'), ('can_create_user', 'Peut créer et gérer des Utilisateurs'))},
        ),
    ]
