# Generated by Django 4.2.3 on 2023-07-31 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataSeeding', '0005_elevatorrequesttype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElevatorRequestStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
    ]
