# Generated by Django 5.0.2 on 2024-02-15 06:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderaddress',
            name='alternativeNo',
        ),
        migrations.RemoveField(
            model_name='orderaddress',
            name='fullname',
        ),
        migrations.RemoveField(
            model_name='orderaddress',
            name='landmark',
        ),
        migrations.RemoveField(
            model_name='orderaddress',
            name='location',
        ),
        migrations.RemoveField(
            model_name='orderaddress',
            name='phoneNumber',
        ),
        migrations.CreateModel(
            name='RequestAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=150, null=True)),
                ('location', models.CharField(blank=True, max_length=150, null=True)),
                ('landmark', models.CharField(blank=True, max_length=150, null=True)),
                ('phoneNumber', models.CharField(blank=True, max_length=150, null=True)),
                ('alternativeNo', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orderaddress',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request_address', to='order.requestaddress'),
        ),
    ]
