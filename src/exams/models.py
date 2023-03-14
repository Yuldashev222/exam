from django.db import models
from datetime import timedelta
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from groups.models import ClassGroup


class Exam(models.Model):
    current = _('current')
    intermediate = _('intermediate')
    final = _('final')

    EXAM_TYPES = (
        ('c', current),
        ('i', intermediate),
        ('f', final)
    )

    SEMESTERS = (
        (1, 'I'), (2, 'II'), (3, 'III'), (4, 'IV'), (5, 'V'), (6, 'VI'), (7, 'VII'), (8, 'VIII')
    )

    title = models.CharField(max_length=400, blank=True)  # or required
    exam_type = models.CharField(max_length=1, choices=EXAM_TYPES)
    allotted_time = models.FloatField(validators=[MinValueValidator(5)], help_text=_('Enter in minutes.'))
    desc = models.TextField(max_length=50000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)
    semester = models.PositiveSmallIntegerField(choices=SEMESTERS)

    def __str__(self):
        return self.get_exam_type_display()

    def save(self, *args, **kwargs):
        self.allotted_time = round(self.allotted_time, 2)
        super().save(*args, **kwargs)


class ExamItem(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True)  # or CASCADE
    group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)  # or SET_NULL
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    desc = models.CharField(max_length=500, blank=True, help_text=_('information to the group about the exam'))

    def __str__(self):
        return f'{self.exam} - {self.group}'

    class Meta:
        verbose_name = _('Exam Item')
        verbose_name_plural = _('Exam Items')

    def clean(self):
        if self.start_date + timedelta(minutes=5) >= self.end_date:
            raise ValidationError(
                {'start_date': _('the start time must be less than the end time')}
            )


class Question(models.Model):
    text = models.CharField(max_length=500)
    image = models.ImageField(upload_to='questions/images/%Y-%m-%d/', blank=True, null=True)  # or FileField
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # or SET_NULL

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['text', 'exam']


class Variant(models.Model):
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['text', 'question']

    def clean(self):
        if self.is_correct and self.question.variant_set.filter(is_correct=True).exists():
            raise ValidationError(
                {'question': _('Bu savolda togri variant mavjud')}
            )


class StudentResult(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # or SET_NULL
    exam_item = models.ForeignKey(ExamItem, on_delete=models.SET_NULL, null=True)
    ball = models.FloatField()
    attempt = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ball}% - {self.student.get_username()}'


class StudentWrongAnswer(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # or SET_NULL
    exam_item = models.ForeignKey(ExamItem, on_delete=models.CASCADE)
    attempt = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)], default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.variant.text
