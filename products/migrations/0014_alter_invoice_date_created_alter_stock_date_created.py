# Generated by Django 4.2.3 on 2024-03-12 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_alter_invoice_date_created_alter_stock_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_created',
            field=models.CharField(default='29-Falgun-2080', editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='stock',
            name='date_created',
            field=models.CharField(default='29-Falgun-2080', max_length=50),
        ),
    ]
