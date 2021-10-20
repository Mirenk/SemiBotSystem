# Generated by Django 3.2.7 on 2021-10-20 05:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semi_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrequest',
            name='rematching_duration',
            field=models.DurationField(null=True),
        ),
        migrations.AlterField(
            model_name='taskrequest',
            name='bachelor_num',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='taskrequest',
            name='master_num',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]