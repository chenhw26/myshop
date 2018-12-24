# Generated by Django 2.1.4 on 2018-12-19 09:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Available',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=15)),
                ('found_date', models.DateField()),
                ('net', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('buy_id', models.AutoField(primary_key=True, serialize=False)),
                ('buy_time', models.DateField(auto_now_add=True)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('computer_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('cpu', models.CharField(max_length=15)),
                ('graphics_card', models.CharField(blank=True, max_length=15, null=True)),
                ('memory', models.IntegerField(validators=[django.core.validators.MaxValueValidator(128), django.core.validators.MinValueValidator(0)])),
                ('ssd_capacity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('disk_capacity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('screen_size', models.CharField(max_length=10)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='computer_comment',
            fields=[
                ('computer_comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('comment_date', models.DateField(auto_now_add=True)),
                ('content', models.TextField()),
                ('computer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Computer')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('coupon_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Brand')),
            ],
        ),
        migrations.CreateModel(
            name='mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark_date', models.DateField(auto_now_add=True)),
                ('computer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Computer')),
            ],
        ),
        migrations.CreateModel(
            name='Own_coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Coupon')),
            ],
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('onsell_date', models.DateField(auto_now_add=True)),
                ('computer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Computer')),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('seller_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('balance', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('shop_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('open_date', models.DateField()),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Seller')),
            ],
        ),
        migrations.CreateModel(
            name='Shop_comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop')),
            ],
        ),
        migrations.CreateModel(
            name='shopping_cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Sell')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('address', models.CharField(max_length=50)),
                ('balance', models.FloatField(default=100000, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.AddField(
            model_name='shopping_cart',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='shop_comment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='sell',
            name='shop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='own_coupon',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='mark',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='like',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='computer_comment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='buy',
            name='computer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Computer'),
        ),
        migrations.AddField(
            model_name='buy',
            name='shop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AddField(
            model_name='buy',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.User'),
        ),
        migrations.AddField(
            model_name='available',
            name='coupon_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Coupon'),
        ),
        migrations.AddField(
            model_name='available',
            name='shop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Shop'),
        ),
        migrations.AlterUniqueTogether(
            name='sell',
            unique_together={('computer_id', 'shop_id')},
        ),
        migrations.AlterUniqueTogether(
            name='own_coupon',
            unique_together={('user_id', 'coupon_id')},
        ),
        migrations.AlterUniqueTogether(
            name='mark',
            unique_together={('user_id', 'computer_id')},
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user_id', 'brand_name')},
        ),
        migrations.AlterUniqueTogether(
            name='available',
            unique_together={('shop_id', 'coupon_id')},
        ),
    ]