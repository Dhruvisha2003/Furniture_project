# Generated by Django 5.0.3 on 2024-08-30 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_blogs'),
    ]

    operations = [
        migrations.CreateModel(
            name='shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=20)),
                ('price', models.CharField(max_length=10)),
            ],
        ),
    ]
