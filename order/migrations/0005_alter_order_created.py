# Generated by Django 4.2.3 on 2024-03-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created',
            field=models.CharField(default='21-Falgun-2080', editable=False, max_length=50),
        ),
    ]
