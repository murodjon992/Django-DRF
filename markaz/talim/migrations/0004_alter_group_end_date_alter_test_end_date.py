# Generated by Django 5.0.2 on 2024-04-21 10:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talim', '0003_alter_group_end_date_alter_test_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 21, 10, 33, 0, 126696, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='test',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 24, 10, 33, 0, 127689, tzinfo=datetime.timezone.utc)),
        ),
    ]
