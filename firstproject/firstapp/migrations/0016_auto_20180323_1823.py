# Generated by Django 2.0.3 on 2018-03-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0015_auto_20180323_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='epoch',
            field=models.CharField(default='', max_length=2047),
        ),
    ]