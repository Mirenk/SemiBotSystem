# Generated by Django 3.2.7 on 2021-10-10 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0002_auto_20211008_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='require_label_value',
            field=models.ManyToManyField(blank=True, related_name='require_task', to='data_manager.LabelValue'),
        ),
    ]
