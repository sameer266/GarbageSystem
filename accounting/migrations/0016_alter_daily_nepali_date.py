# Generated by Django 4.2.3 on 2024-03-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0015_alter_daily_nepali_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='nepali_date',
            field=models.CharField(default='15-Chaitra-2080', max_length=50),
        ),
    ]
