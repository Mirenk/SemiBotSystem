# Generated by Django 3.2.7 on 2021-10-18 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0004_auto_20211017_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrequestrequest',
            name='cancel_url',
            field=models.URLField(default='http://example.com'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskrequestrequest',
            name='join_complete_message',
            field=models.TextField(default='msg'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskrequestrequest',
            name='join_url',
            field=models.URLField(default='http://example.com'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='taskrequestrequest',
            name='request_message',
            field=models.TextField(default='msg'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taskrequestrequest',
            name='callback_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
