# Generated by Django 2.0.3 on 2018-03-23 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0019_auto_20180323_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='epoch',
            field=models.CharField(default='0', max_length=2047),
        ),
    ]