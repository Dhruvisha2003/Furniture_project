# Generated by Django 5.0.3 on 2024-09-14 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0013_bill_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_address',
            name='ordernotes',
        ),
    ]
