# Generated by Django 3.0.8 on 2020-08-19 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='user',
            new_name='pic_by',
        ),
    ]