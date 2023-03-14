from django.contrib import admin

from .models import Exam, Question, Variant, StudentResult, StudentWrongAnswer, ExamItem


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['exam_type', 'semester', 'allotted_time', 'attempts', 'date_created']
    list_display_links = list_display
    list_filter = ['exam_type', 'semester']
    search_fields = ['title', 'desc']
    fields = [
        'title',
        'semester',
        'exam_type',
        'allotted_time',
        'attempts',
        'desc'
    ]


@admin.register(ExamItem)
class ExamItemAdmin(admin.ModelAdmin):
    list_display = ['exam_type', 'semester', 'group', 'start_date', 'end_date']
    list_display_links = list_display
    list_filter = ['exam__exam_type', 'exam__semester', 'group']

    @admin.display
    def exam_type(self, obj):
        return obj.exam.get_exam_type_display()

    @admin.display
    def semester(self, obj):
        return obj.exam.get_semester_display()

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exam', 'group')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exam', 'text', 'image']
    list_filter = ['exam', 'exam__semester']
    search_fields = ['text']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('exam')


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_correct']
    list_display_links = list_display
    list_filter = ['question__exam', 'question__exam__semester']
    search_fields = ['text']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('question__exam')


@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'group', 'exam_item', 'semester', 'attempt', 'ball', 'date_created'
    ]
    list_display_links = list_display
    search_fields = ['student__email', 'student__first_name', 'student__last_name']
    list_filter = ['exam_item__exam', 'exam_item__exam__semester', 'exam_item', 'attempt']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'student__group', 'exam_item__exam')

    @admin.display
    def email(self, obj):
        return obj.student.email

    @admin.display
    def semester(self, obj):
        return obj.exam_item.exam.get_semester_display()

    @admin.display
    def group(self, obj):
        return obj.student.group

    @admin.display
    def first_name(self, obj):
        return obj.student.first_name

    @admin.display
    def last_name(self, obj):
        return obj.student.last_name


@admin.register(StudentWrongAnswer)
class StudentWrongAnswerAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'group', 'exam_item', 'attempt', 'semester', 'variant'
    ]
    list_display_links = list_display
    search_fields = ['variant__text', 'student__email', 'student__first_name', 'student__last_name']
    list_filter = ['exam_item__exam', 'exam_item__exam__semester', 'exam_item', 'attempt']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'student__group', 'variant', 'exam_item__exam')

    @admin.display
    def email(self, obj):
        return obj.student.email

    @admin.display
    def semester(self, obj):
        return obj.exam_item.exam.get_semester_display()

    @admin.display
    def group(self, obj):
        return obj.student.group

    @admin.display
    def first_name(self, obj):
        return obj.student.first_name

    @admin.display
    def last_name(self, obj):
        return obj.student.last_name
