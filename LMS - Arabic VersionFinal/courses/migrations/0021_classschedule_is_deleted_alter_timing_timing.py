# Generated by Django 4.2.1 on 2023-09-05 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_user_alter_topic_t_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='classschedule',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timing',
            name='timing',
            field=models.CharField(max_length=128),
        ),
    ]
