# Generated by Django 2.1.4 on 2018-12-20 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shop_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='computer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Computer'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='shop_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Shop'),
        ),
        migrations.AlterField(
            model_name='buy',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.User'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.Brand'),
        ),
        migrations.AlterField(
            model_name='computer_comment',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.User'),
        ),
        migrations.AlterField(
            model_name='shop_comment',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.User'),
        ),
    ]
