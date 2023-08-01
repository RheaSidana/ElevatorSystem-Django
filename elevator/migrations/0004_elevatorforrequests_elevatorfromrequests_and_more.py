# Generated by Django 4.2.3 on 2023-08-01 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataSeeding', '0006_elevatorrequeststatus'),
        ('elevator', '0003_alter_elevatorrequests_req_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElevatorForRequests',
            fields=[
                ('reqID', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('req_time', models.DateTimeField(auto_now_add=True)),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_for', to='elevator.elevator')),
                ('floor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestOn', to='elevator.floor')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_status', to='dataSeeding.elevatorrequeststatus')),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorFromRequests',
            fields=[
                ('reqID', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('req_time', models.DateTimeField(auto_now_add=True)),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_from', to='elevator.elevator')),
                ('from_floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_from_floor', to='elevator.floor')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_from_status', to='dataSeeding.elevatorrequeststatus')),
                ('to_floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_to_floor', to='elevator.floor')),
            ],
        ),
        migrations.DeleteModel(
            name='ElevatorRequests',
        ),
    ]