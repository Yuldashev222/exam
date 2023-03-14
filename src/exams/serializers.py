from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import ExamItem, Exam, Question, Variant, StudentResult


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        exclude = ['id']


class ExamItemSerializer(serializers.ModelSerializer):
    exam_type = serializers.CharField(source='exam.get_exam_type_display')
    semester = serializers.CharField(source='exam.get_semester_display')
    title = serializers.CharField(source='exam.title')
    allotted_time = serializers.FloatField(source='exam.allotted_time')
    exam_desc = serializers.CharField(source='exam.desc')
    for_group_desc = serializers.CharField(source='desc')
    date_created = serializers.DateTimeField(source='exam.date_created')
    attempts = serializers.IntegerField(source='exam.attempts')

    class Meta:
        model = ExamItem
        exclude = ['group', 'exam']


class VariantSerializer(serializers.Serializer):
    text = serializers.CharField()
    id = serializers.IntegerField()


class QuestionSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(source='variant_set', many=True)

    class Meta:
        model = Question
        exclude = ['exam']


class ExamStartSerializer(ExamItemSerializer):
    questions = QuestionSerializer(source='exam.question_set', many=True)


class StudentResultSerializer(serializers.ModelSerializer):
    exam_item = ExamItemSerializer()

    class Meta:
        model = StudentResult
        exclude = ['id', 'student']


class QuestionVariantIDSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    variant_id = serializers.IntegerField()

    def validate(self, attrs):
        question = Question.objects.filter(id=attrs['question_id'])
        if not question.exists():
            raise NotFound({'question_id': ['question not found']})

        exam_item = ExamItem.objects.get(pk=self.context['exam_item_id'])
        if not exam_item.exam.question_set.filter(id=question.first().id).exists():
            raise NotFound({'question_id': ['question not found in exam item']})

        variant = Variant.objects.filter(id=attrs['variant_id'])
        if not variant.exists():
            raise NotFound({'variant_id': ['variant not found']})

        if not question.first().variant_set.filter(id=attrs['variant_id']).exists():
            raise NotFound({'variant_id': ['variant not found in question']})
        return attrs


[
    {"question_id": 1, "variant_id": 1},
    {"question_id": 1, "variant_id": 2}
]
