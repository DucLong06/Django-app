# Generated by Django 4.0.1 on 2022-02-08 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_rating_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
            ],
        ),
    ]
