from rest_framework import permissions

from .models import ExamItem


class IsStudentExam(permissions.BasePermission):
    def has_permission(self, request, view):
        exam_item = ExamItem.objects.filter(pk=view.kwargs.get('exam_item_id'))
        return exam_item.exists() and exam_item.first().group_id == request.user.group.id


class IsNotAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff
