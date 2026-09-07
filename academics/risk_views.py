from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .risk_service import predict_risk_for_student
from .models import RiskAssessment


class MyRiskAssessmentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        student = request.user
        risk_level, advice_text, features = predict_risk_for_student(student)

        assessment = RiskAssessment.objects.create(
            student=student,
            risk_level=risk_level,
            average_mark=features["average_mark"],
            attendance_rate=features["attendance_rate"],
            modules_failed_count=features["modules_failed_count"],
            advice_text=advice_text,
        )

        student.student_profile.current_risk_level = risk_level
        student.student_profile.save(update_fields=["current_risk_level"])

        return Response({
            "risk_level": risk_level,
            "advice_text": advice_text,
            "computed_at": assessment.computed_at,
            "features_used": features,
        })


class MyRiskHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        history = RiskAssessment.objects.filter(student=request.user).order_by("computed_at")
        return Response([
            {
                "computed_at": r.computed_at,
                "risk_level": r.risk_level,
                "average_mark": r.average_mark,
            }
            for r in history
        ])