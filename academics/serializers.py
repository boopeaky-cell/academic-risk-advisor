from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile
from .models import Module, Enrollment, Mark

User = get_user_model()


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'assessment_name', 'weight_percent', 'score_percent', 'date_recorded']


class MarkUploadSerializer(serializers.Serializer):
    student_number = serializers.CharField()
    module_code = serializers.CharField()
    year = serializers.IntegerField()
    assessment_name = serializers.CharField(max_length=100)
    weight_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    score_percent = serializers.DecimalField(max_digits=5, decimal_places=2)

    def validate_student_number(self, value):
        if not User.objects.filter(student_number=value, role='student').exists():
            raise serializers.ValidationError("No student found with this student number.")
        return value

    def validate_module_code(self, value):
        if not Module.objects.filter(code=value).exists():
            raise serializers.ValidationError("No module found with this code.")
        return value

    def create(self, validated_data):
        student = User.objects.get(student_number=validated_data['student_number'])
        module = Module.objects.get(code=validated_data['module_code'])
        enrollment, _ = Enrollment.objects.get_or_create(
            student=student, module=module, year=validated_data['year'],
            defaults={'status': 'active'}
        )
        return Mark.objects.create(
            enrollment=enrollment,
            assessment_name=validated_data['assessment_name'],
            weight_percent=validated_data['weight_percent'],
            score_percent=validated_data['score_percent'],
            uploaded_by=self.context['request'].user,
        )


class StudentPerformanceSerializer(serializers.ModelSerializer):
    student_number = serializers.CharField(source='user.student_number')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = StudentProfile
        fields = ['student_number', 'first_name', 'last_name', 'level_of_study',
                  'programme', 'current_risk_level', 'credits_completed', 'credits_required']