# Generated by Django 4.2.1 on 2023-09-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0035_remove_timing_class_duration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classentry',
            name='users',
            field=models.ManyToManyField(through='courses.Commitment', to='courses.user'),
        ),
        migrations.AddConstraint(
            model_name='suspensiontime',
            constraint=models.UniqueConstraint(condition=models.Q(('is_deleted', False)), fields=('course',), name='course_suspend_key'),
        ),
    ]