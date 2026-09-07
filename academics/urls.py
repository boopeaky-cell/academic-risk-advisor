from django.urls import path
from .risk_views import MyRiskAssessmentView, MyRiskHistoryView
from .module_performance_view import ModulePerformanceView

urlpatterns = [
    path('my-risk/', MyRiskAssessmentView.as_view(), name='my-risk'),
    path('my-risk-history/', MyRiskHistoryView.as_view(), name='my-risk-history'),
    path('my-module-performance/', ModulePerformanceView.as_view(), name='my-module-performance'),
]