# Generated by Django 4.2.1 on 2023-11-15 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0036_alter_classentry_users_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commitment',
            name='role',
            field=models.CharField(choices=[('PRIMARY', 'PRIMARY'), ('ASSISTANT', 'ASSISTANT')], max_length=128),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.user')),
            ],
            options={
                'db_table': 'experiences',
            },
        ),
    ]
