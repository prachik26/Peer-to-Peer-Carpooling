# Generated by Django 4.1.7 on 2023-05-16 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_booking_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mycar',
            name='car_num',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
