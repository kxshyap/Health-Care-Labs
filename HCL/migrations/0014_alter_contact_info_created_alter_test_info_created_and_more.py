# Generated by Django 4.1.3 on 2023-02-11 09:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCL', '0013_alter_contact_info_created_alter_test_info_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 11, 15, 3, 59, 582149)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 11, 15, 3, 59, 582149)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='status',
            field=models.CharField(blank=True, choices=[(1, 'Pending'), (2, 'Done')], default=1, max_length=20),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 11, 15, 3, 59, 582149)),
        ),
    ]