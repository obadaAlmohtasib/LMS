# Generated by Django 4.2.1 on 2023-09-04 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0017_alter_commitment_role_alter_timing_timing'),
    ]

    operations = [
        migrations.AddField(
            model_name='classlecturer',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='classsupervisor',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commitment',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
