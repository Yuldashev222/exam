from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated

from .models import Exam, ExamItem, StudentResult, Variant, StudentWrongAnswer
from .permissions import IsNotAdminUser

from .serializers import (
    ExamItemSerializer,
    ExamSerializer,
    ExamStartSerializer,
    StudentResultSerializer,
    QuestionVariantIDSerializer
)


class ExamAPIView(ListAPIView):
    queryset = Exam.objects.all().order_by('-date_created')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]


class StudentExamAPIView(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsNotAdminUser]

    def get_serializer_class(self):
        return ExamItemSerializer if self.action == 'list' else ExamStartSerializer

    def get_queryset(self):
        student = self.request.user
        queryset = ExamItem.objects.filter(
            group_id=student.group.id
        ).select_related('exam')
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('exam__question_set', 'exam__question_set__variant_set')
        return queryset


class StudentResultAPIView(ListAPIView):
    serializer_class = StudentResultSerializer
    permission_classes = [IsAuthenticated, IsNotAdminUser]

    def get_queryset(self):
        student = self.request.user
        queryset = StudentResult.objects.filter(student_id=student.id).select_related(
            'exam_item', 'exam_item__exam'
        ).order_by('-date_created')
        return queryset


class SaveResultAPIView(APIView):
    permission_classes = [IsAuthenticated, IsNotAdminUser]

    def post(self, request, exam_item_id):
        exam_item = get_object_or_404(ExamItem, pk=exam_item_id)
        questions = exam_item.exam.question_set.all()

        if not isinstance(request.data, list):
            raise ValidationError('')
        elif len(request.data) > questions.count():
            raise ValidationError('')

        student = self.request.user
        if exam_item.group_id != student.group_id:
            raise NotFound()
        max_attempt = StudentResult.objects.filter(
            student_id=student.id,
            exam_item_id=exam_item.id
        ).aggregate(max_attempt=Max('attempt'))['max_attempt']
        if max_attempt and max_attempt >= exam_item.exam.attempts:
            raise PermissionDenied()

        serializer = QuestionVariantIDSerializer(data=request.data, many=True, context={'exam_item_id': exam_item_id})
        serializer.is_valid(raise_exception=True)

        variant_ids = [item['variant_id'] for item in serializer.initial_data]
        correct_variants = Variant.objects.filter(id__in=variant_ids, is_correct=True)
        result = StudentResult.objects.create(
            student_id=student.id,
            exam_item_id=exam_item.id,
            ball=round(correct_variants.count() / questions.count(), 2),
            attempt=max_attempt + 1
        )
        wrong_variants = Variant.objects.filter(id__in=variant_ids, is_correct=False)
        wrong_answers = [
            StudentWrongAnswer(
                student_id=student.id,
                exam_item_id=exam_item.id,
                question_id=variant.question.id,
                attempt=max_attempt + 1,
                variant_id=variant.id,
            )
            for variant in wrong_variants
        ]
        if questions.count() > correct_variants.count() + wrong_variants.count():
            questions = questions.exclude(variant__in=wrong_variants + correct_variants)
            second_wrong_answers = [
                StudentWrongAnswer(
                    student_id=student.id,
                    exam_item_id=exam_item.id,
                    question_id=question.id,
                    attempt=max_attempt + 1
                )
                for question in questions
            ]
            wrong_answers += second_wrong_answers
        StudentWrongAnswer.objects.bulk_create(wrong_answers)
        return Response({'ball': result.ball, 'attempt': result.attempt}, status=HTTP_201_CREATED)
