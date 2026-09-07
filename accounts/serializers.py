from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile

User = get_user_model()


class StudentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    level_of_study = serializers.IntegerField(write_only=True)
    programme = serializers.CharField(write_only=True, default="Computer Science")

    class Meta:
        model = User
        fields = ['student_number', 'first_name', 'last_name', 'password',
                  'level_of_study', 'programme']

    def create(self, validated_data):
        level_of_study = validated_data.pop('level_of_study')
        programme = validated_data.pop('programme')
        password = validated_data.pop('password')

        user = User(
            username=validated_data['student_number'],
            role='student',
            **validated_data
        )
        user.set_password(password)
        user.save()

        StudentProfile.objects.create(
            user=user, level_of_study=level_of_study, programme=programme
        )
        return user


class StudentProfileSerializer(serializers.ModelSerializer):
    student_number = serializers.CharField(source='user.student_number', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['student_number', 'first_name', 'last_name', 'level_of_study',
                  'programme', 'credits_completed', 'credits_required', 'current_risk_level']