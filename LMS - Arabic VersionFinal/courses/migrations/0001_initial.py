# Generated by Django 4.2.1 on 2023-06-24 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_num', models.SmallIntegerField()),
                ('entry_date', models.DateTimeField()),
                ('place', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Commitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Primary', 'Primary'), ('Secondary-1', 'Secondary-1'), ('Secondary-2', 'Secondary-2')], max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('no_of_classes', models.IntegerField()),
                ('no_daily_classes', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('break_time', models.TimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('no_of_classes', models.IntegerField()),
                ('typeOf', models.CharField(choices=[('ACADEMIC', 'Academic'), ('NON-ACADEMIC', 'Non-Academic'), ('EXAM', 'Exam')], max_length=128)),
                ('training_facility', models.CharField(choices=[('A_1', 'A_1'), ('B_2', 'B_2'), ('C_3', 'C_3'), ('D_4', 'D_4')], max_length=128)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='PublicHolidays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('event_name', models.CharField(max_length=128)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('courses', models.ManyToManyField(through='courses.Commitment', to='courses.course')),
            ],
        ),
        migrations.CreateModel(
            name='ExamSupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.topic')),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='Institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.institution'),
        ),
        migrations.AddField(
            model_name='commitment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='commitment',
            name='lecturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lecturer'),
        ),
        migrations.CreateModel(
            name='ClassSupervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.classentry')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.examsupervisor')),
            ],
        ),
        migrations.CreateModel(
            name='ClassLecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.classentry')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.lecturer')),
            ],
        ),
        migrations.AddField(
            model_name='classentry',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.course'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='course_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.coursegroup'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='exam_supervisors',
            field=models.ManyToManyField(blank=True, null=True, through='courses.ClassSupervisor', to='courses.examsupervisor'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='lecturers',
            field=models.ManyToManyField(blank=True, null=True, through='courses.ClassLecturer', to='courses.lecturer'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.topic'),
        ),
    ]
