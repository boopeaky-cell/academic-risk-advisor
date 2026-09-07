from django.urls import path
from .risk_views import MyRiskAssessmentView, MyRiskHistoryView
from .module_performance_view import ModulePerformanceView
from .lecturer_views import UploadMarkView, StudentListView, StudentPerformanceDetailView

urlpatterns = [
    path('my-risk/', MyRiskAssessmentView.as_view(), name='my-risk'),
    path('my-risk-history/', MyRiskHistoryView.as_view(), name='my-risk-history'),
    path('my-module-performance/', ModulePerformanceView.as_view(), name='my-module-performance'),
    path('lecturer/upload-mark/', UploadMarkView.as_view(), name='lecturer-upload-mark'),
    path('lecturer/students/', StudentListView.as_view(), name='lecturer-students'),
    path('lecturer/students/<str:student_number>/', StudentPerformanceDetailView.as_view(), name='lecturer-student-detail'),
]