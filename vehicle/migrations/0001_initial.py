# Generated by Django 5.0.6 on 2024-05-21 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MapPopup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('route', models.CharField(max_length=255)),
                ('plate_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RealTimecoords',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
    ]
