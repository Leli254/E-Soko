# Generated by Django 4.1.2 on 2022-10-11 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='phone_number',
        ),
    ]