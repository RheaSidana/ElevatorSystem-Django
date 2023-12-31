# Generated by Django 4.2.3 on 2023-07-31 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataSeeding', '0006_elevatorrequeststatus'),
        ('elevator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('name', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('capacity', models.IntegerField()),
                ('requestsCapacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorRequests',
            fields=[
                ('reqID', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('req_time', models.DateTimeField()),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='elevator.elevator')),
                ('floor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requestOn', to='elevator.floor')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_status', to='dataSeeding.elevatorrequeststatus')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='dataSeeding.elevatorrequesttype')),
            ],
        ),
        migrations.CreateModel(
            name='ElevatorFunctionality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curr_req_count', models.IntegerField()),
                ('curr_person_count', models.IntegerField()),
                ('direction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator_direction', to='dataSeeding.moving')),
                ('door_functionality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator_door', to='dataSeeding.doorfunctions')),
                ('elevator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator', to='elevator.elevator')),
                ('floor_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevatorOn', to='elevator.floor')),
                ('movement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator_movement', to='dataSeeding.movements')),
                ('operational_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elevator_operational', to='dataSeeding.operational_status')),
            ],
        ),
    ]
