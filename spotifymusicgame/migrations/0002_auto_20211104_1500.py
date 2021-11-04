# Generated by Django 3.2.7 on 2021-11-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotifymusicgame', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subject_id', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('subject_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='roominfo',
            name='player',
        ),
        migrations.RemoveField(
            model_name='roominfo',
            name='url',
        ),
        migrations.DeleteModel(
            name='played',
        ),
        migrations.DeleteModel(
            name='playList',
        ),
        migrations.DeleteModel(
            name='roomInfo',
        ),
    ]