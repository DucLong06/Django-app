# Generated by Django 4.0.1 on 2022-02-08 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_lessonview_lesson'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonview',
            old_name='view',
            new_name='views',
        ),
    ]