# Generated by Django 4.2.3 on 2023-08-01 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0006_rename_req_time_elevatorforrequests_reqtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elevatorfromrequests',
            old_name='req_time',
            new_name='reqTime',
        ),
    ]
