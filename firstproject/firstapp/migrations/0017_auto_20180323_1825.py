# Generated by Django 2.0.3 on 2018-03-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0016_auto_20180323_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='epoch',
            field=models.IntegerField(default=0),
        ),
    ]