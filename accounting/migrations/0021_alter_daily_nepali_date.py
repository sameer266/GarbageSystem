# Generated by Django 4.2.3 on 2025-04-26 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0020_alter_daily_nepali_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='nepali_date',
            field=models.CharField(default='13-Baishakh-2082', max_length=50),
        ),
    ]
