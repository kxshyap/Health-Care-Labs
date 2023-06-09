# Generated by Django 4.1.3 on 2023-02-13 08:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HCL', '0014_alter_contact_info_created_alter_test_info_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 13, 14, 25, 38, 358110)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 13, 14, 25, 38, 357112)),
        ),
        migrations.AlterField(
            model_name='test_info',
            name='status',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 2, 13, 14, 25, 38, 357112)),
        ),
    ]
