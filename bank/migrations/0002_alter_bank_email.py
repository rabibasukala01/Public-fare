# Generated by Django 5.0.6 on 2024-05-21 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
