# Generated by Django 2.0.3 on 2018-03-23 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0013_auto_20180323_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='port',
            old_name='licenses',
            new_name='license',
        ),
        migrations.RenameField(
            model_name='port',
            old_name='path',
            new_name='portdir',
        ),
    ]