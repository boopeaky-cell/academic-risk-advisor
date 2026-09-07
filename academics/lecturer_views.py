from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile
from accounts.permissions import IsLecturer
from .models import Enrollment
from .serializers import MarkUploadSerializer, MarkSerializer, StudentPerformanceSerializer

User = get_user_model()


class UploadMarkView(APIView):
    permission_classes = [IsLecturer]

    def post(self, request):
        serializer = MarkUploadSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        mark = serializer.save()
        return Response(MarkSerializer(mark).data, status=status.HTTP_201_CREATED)


class StudentListView(APIView):
    permission_classes = [IsLecturer]

    def get(self, request):
        profiles = StudentProfile.objects.select_related('user').all()
        return Response(StudentPerformanceSerializer(profiles, many=True).data)


class StudentPerformanceDetailView(APIView):
    permission_classes = [IsLecturer]

    def get(self, request, student_number):
        try:
            student = User.objects.get(student_number=student_number, role='student')
        except User.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        enrollments = Enrollment.objects.filter(student=student).select_related('module')
        data = [{
            "module_code": e.module.code,
            "module_name": e.module.name,
            "year": e.year,
            "status": e.status,
            "marks": MarkSerializer(e.marks.all(), many=True).data,
        } for e in enrollments]

        return Response({
            "student_number": student.student_number,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "current_risk_level": student.student_profile.current_risk_level,
            "enrollments": data,
        })