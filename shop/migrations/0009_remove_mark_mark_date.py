# Generated by Django 2.1.4 on 2018-12-21 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20181221_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='mark_date',
        ),
    ]