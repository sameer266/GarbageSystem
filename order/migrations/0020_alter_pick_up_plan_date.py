# Generated by Django 5.0.2 on 2024-02-23 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_alter_pick_up_plan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pick_up_plan',
            name='date',
            field=models.CharField(default='11-Falgun-2080', max_length=50),
        ),
    ]
