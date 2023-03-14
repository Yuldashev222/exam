# Generated by Django 3.2.16 on 2023-03-13 18:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=400)),
                ('exam_type', models.CharField(choices=[('c', 'current'), ('i', 'intermediate'), ('f', 'final')], max_length=1)),
                ('allotted_time', models.FloatField(help_text='Enter in minutes.', verbose_name=django.core.validators.MinValueValidator(5))),
                ('desc', models.TextField(blank=True, max_length=50000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('attempts', models.PositiveSmallIntegerField(default=1, verbose_name=django.core.validators.MinValueValidator(1))),
            ],
        ),
        migrations.CreateModel(
            name='ExamItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('desc', models.CharField(blank=True, help_text='information to the group about the exam', max_length=500)),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exams.exam')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.classgroup')),
            ],
            options={
                'verbose_name': 'Exam Item',
                'verbose_name_plural': 'Exam Items',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('image', models.ImageField(blank=True, null=True, upload_to='questions/images/%Y-%m-%d/')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.question')),
            ],
        ),
        migrations.CreateModel(
            name='StudentWrongAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.examitem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.variant')),
            ],
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ball', models.FloatField()),
                ('attempt', models.PositiveSmallIntegerField(default=1, verbose_name=django.core.validators.MinValueValidator(1))),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('exam_item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='exams.examitem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='variant',
            constraint=models.UniqueConstraint(condition=models.Q(('is_correct', True)), fields=('question',), name='unique_question_is_correct_variant'),
        ),
    ]