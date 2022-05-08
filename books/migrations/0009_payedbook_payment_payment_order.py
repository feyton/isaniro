# Generated by Django 4.0.4 on 2022-05-14 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_payedbook_customer_payment_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payedbook',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.payment'),
        ),
        migrations.AddField(
            model_name='payment',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.order'),
        ),
    ]