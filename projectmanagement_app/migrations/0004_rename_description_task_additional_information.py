# Generated by Django 4.0.4 on 2022-07-29 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanagement_app', '0003_project_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='description',
            new_name='additional_information',
        ),
    ]
