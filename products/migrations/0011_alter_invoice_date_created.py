# Generated by Django 4.2.3 on 2024-03-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_invoice_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='date_created',
            field=models.CharField(default='21-Falgun-2080', editable=False, max_length=50),
        ),
    ]
