# Generated by Django 3.1.7 on 2021-04-13 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='userID'),
        ),
    ]
