# Generated by Django 3.0.10 on 2020-09-26 11:46

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuidfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('random_code', shortuuidfield.fields.ShortUUIDField(blank=True, default=app.models.Class.code, editable=False, max_length=22)),
                ('subject', models.CharField(max_length=200, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EnterCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years', models.CharField(max_length=20)),
                ('department', models.ManyToManyField(to='app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leaveFromDate', models.DateField()),
                ('leaveTillDate', models.DateField()),
                ('leaveReason', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('studentClass', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.Class')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Department'),
        ),
        migrations.AddField(
            model_name='class',
            name='student',
            field=models.ManyToManyField(to='account.Student'),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='class',
            name='years',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Year'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Class')),
                ('student', models.ManyToManyField(to='account.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
