# Generated by Django 4.2.1 on 2023-09-04 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_classentry_is_deleted_course_is_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsupervisor',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicholidays',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='timing',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
