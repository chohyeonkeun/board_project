# Generated by Django 2.1 on 2019-04-25 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockrank',
            name='rank_num',
        ),
    ]
