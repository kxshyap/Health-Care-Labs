# Generated by Django 4.1.3 on 2023-02-04 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCL', '0009_alter_contact_info_created_alter_test_info_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 4, 13, 18, 33, 696983)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 4, 13, 18, 33, 696026)),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 4, 13, 18, 33, 696026)),
        ),
    ]
