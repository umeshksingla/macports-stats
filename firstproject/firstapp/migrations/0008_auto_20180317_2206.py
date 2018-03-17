# Generated by Django 2.0.3 on 2018-03-17 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_auto_20180317_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_handle', models.CharField(max_length=255, null=True, unique=True)),
                ('email', models.CharField(max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='installedport',
            old_name='variants',
            new_name='installed_variants',
        ),
        migrations.RenameField(
            model_name='installedport',
            old_name='version',
            new_name='installed_version',
        ),
        migrations.AddField(
            model_name='port',
            name='epoch',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='port',
            name='exists',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='port',
            name='long_description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='port',
            name='revision',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='port',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.RemoveField(
            model_name='port',
            name='maintainers',
        ),
        migrations.AddField(
            model_name='port',
            name='maintainers',
            field=models.ManyToManyField(to='firstapp.Maintainer'),
        ),
    ]
