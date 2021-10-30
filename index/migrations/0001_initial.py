# Generated by Django 3.2.8 on 2021-10-30 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
                ('date_subscribed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Uwiyandikishije',
                'verbose_name_plural': 'Abiyandikishije',
                'ordering': ['-name'],
            },
        ),
    ]
