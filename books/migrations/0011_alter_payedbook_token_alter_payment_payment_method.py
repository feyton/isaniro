# Generated by Django 4.0.4 on 2022-05-14 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_alter_book_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payedbook',
            name='token',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default='mobilemoney', max_length=50),
        ),
    ]
