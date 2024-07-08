# Generated by Django 4.2.1 on 2023-12-03 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0039_trainingcourse_scientificdegree_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='validity',
            field=models.SmallIntegerField(choices=[(-1, 'For Ever'), (1, 'One Year'), (5, 'Five Years')]),
        ),
        migrations.AlterField(
            model_name='scientificdegree',
            name='sci_degree',
            field=models.CharField(choices=[('HIGH_SCHOOL', 'HIGH_SCHOOL'), ('DIPLOMA', 'DIPLOMA'), ('BACHELOR', 'BACHELOR'), ('MASTER', 'MASTER'), ('DOCTORAL', 'DOCTORAL')], max_length=128),
        ),
    ]
