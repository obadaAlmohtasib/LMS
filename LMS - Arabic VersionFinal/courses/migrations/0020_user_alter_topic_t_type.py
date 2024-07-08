# Generated by Django 4.2.1 on 2023-09-05 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_alter_classentry_exam_supervisors_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('source', models.CharField(choices=[('INTERNAL', 'INTERNAL'), ('CONTRACTED', 'CONTRACTED'), ('EXTERNAL', 'EXTERNAL')], max_length=128)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AlterField(
            model_name='topic',
            name='t_type',
            field=models.CharField(choices=[('ACADEMIC', 'ACADEMIC'), ('NON-ACADEMIC', 'NON-ACADEMIC'), ('EXAM', 'EXAM'), ('INITIAL', 'INITIAL')], db_column='t_type', max_length=128),
        ),
    ]
