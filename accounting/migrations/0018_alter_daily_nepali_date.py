# Generated by Django 4.2.3 on 2024-05-02 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0017_alter_daily_nepali_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='nepali_date',
            field=models.CharField(default='20-Baishakh-2081', max_length=50),
        ),
    ]
