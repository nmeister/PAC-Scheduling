# Generated by Django 3.0.4 on 2020-05-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pacApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyrequest',
            name='request_id',
            field=models.CharField(default=0, max_length=50, unique=True),
        ),
    ]
