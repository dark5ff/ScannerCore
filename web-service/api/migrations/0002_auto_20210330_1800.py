# Generated by Django 3.1.7 on 2021-03-30 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detectedurl',
            old_name='referer',
            new_name='crawlerName',
        ),
    ]