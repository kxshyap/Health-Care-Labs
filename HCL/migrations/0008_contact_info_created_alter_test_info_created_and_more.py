# Generated by Django 4.1.3 on 2023-01-30 10:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCL', '0007_alter_test_info_created_alter_user_info_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 30, 15, 34, 32, 499370)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 30, 15, 34, 32, 499370)),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 30, 15, 34, 32, 499370)),
        ),
    ]
