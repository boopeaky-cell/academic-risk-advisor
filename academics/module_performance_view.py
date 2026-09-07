from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum

from .models import Enrollment


class ModulePerformanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user).select_related('module')
        results = []

        for enrollment in enrollments:
            marks = enrollment.marks.all()
            total_weight = marks.aggregate(w=Sum('weight_percent'))['w'] or 0

            if total_weight > 0:
                weighted_sum = sum(
                    (m.score_percent * m.weight_percent) for m in marks
                )
                weighted_average = round(weighted_sum / total_weight, 1)
            else:
                weighted_average = None

            results.append({
                "module_code": enrollment.module.code,
                "module_name": enrollment.module.name,
                "year": enrollment.year,
                "status": enrollment.status,
                "weighted_average": weighted_average,
                "assessments_recorded": marks.count(),
                "at_risk_in_module": weighted_average is not None and weighted_average < 50,
            })

        return Response(results)