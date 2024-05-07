# Generated by Django 5.0.2 on 2024-04-23 12:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talim', '0007_banner_murojaat_testimonial_alter_group_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='body_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='body_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='body_uz',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_ru',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='banner',
            name='title_uz',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 23, 12, 52, 34, 739599, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='test',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 26, 12, 52, 34, 740596, tzinfo=datetime.timezone.utc)),
        ),
    ]