# Generated by Django 3.0.4 on 2020-04-12 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacApp', '0005_auto_20200412_1719'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='showtime',
        ),
        migrations.AddField(
            model_name='booking',
            name='week_day',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='end_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='booking',
            name='start_time',
            field=models.IntegerField(),
        ),
    ]