# Generated by Django 4.2.1 on 2024-02-23 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0049_alter_topic_t_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='call',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='identification',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
