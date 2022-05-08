# Generated by Django 4.0.4 on 2022-05-14 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_remove_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payedbook',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='books.customer'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.PositiveIntegerField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_settled',
            field=models.PositiveIntegerField(default=900),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='currency',
            field=models.CharField(default='RWF', max_length=4),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default="345", max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='mobilemoney', max_length=10),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default=234, max_length=20),
            preserve_default=False,
        ),
    ]
