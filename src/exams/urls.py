from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import StudentExamAPIView, ExamAPIView, StudentResultAPIView, SaveResultAPIView

urlpatterns = [
    path('results/', StudentResultAPIView.as_view()),
    path('results/save/<int:exam_item_id>/', SaveResultAPIView.as_view()),
    path('', ExamAPIView.as_view()),
]

router = SimpleRouter()
router.register('items', StudentExamAPIView, basename='exam-item')

urlpatterns += router.urls
