# Generated by Django 3.2.8 on 2022-01-04 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20220103_1144'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_on', '-published_date'], 'verbose_name': 'blog'},
        ),
    ]
