# Generated by Django 3.2.4 on 2021-06-12 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('facid', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('dept', models.CharField(max_length=4)),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('office_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('office_section', models.CharField(max_length=50)),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('usn', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('dept', models.CharField(max_length=4)),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=256, unique=True)),
                ('facid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculties', to='student.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Requisitions',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('reqid', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('phone', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=256)),
                ('date', models.DateTimeField()),
                ('subject', models.TextField(max_length=50)),
                ('office_section', models.TextField(max_length=30)),
                ('issue', models.TextField(max_length=30)),
                ('reason', models.TextField(max_length=100)),
                ('proc_appr', models.PositiveIntegerField(default=0)),
                ('hod_appr', models.PositiveIntegerField(default=0)),
                ('office_appr', models.PositiveIntegerField(default=0)),
                ('facid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.faculty')),
                ('usn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]