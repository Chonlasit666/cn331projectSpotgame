# Generated by Django 3.2.7 on 2021-11-05 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotifymusicgame', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roominfo',
            name='ready_player',
        ),
    ]
