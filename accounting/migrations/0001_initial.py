# Generated by Django 5.0.2 on 2024-02-21 05:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nepali_date', models.CharField(max_length=200)),
                ('total', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-nepali_date'],
            },
        ),
        migrations.CreateModel(
            name='DailyTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField()),
                ('remarks', models.TextField()),
                ('dailyid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dailyId', to='accounting.daily')),
                ('product', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='daily_product', to='products.product')),
                ('unite', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='daily_product_unit', to='products.unit')),
            ],
            options={
                'ordering': ['-dailyid'],
            },
        ),
    ]
