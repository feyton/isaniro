# Generated by Django 3.2.8 on 2021-10-30 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_thumbnail_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail_image',
            field=models.ImageField(blank=True, default='/blog/default_thumb.jpg', null=True, upload_to='blog/thumnails'),
        ),
    ]
