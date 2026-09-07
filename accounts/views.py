
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import StudentProfile
from .serializers import StudentRegisterSerializer, StudentProfileSerializer


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegisterSerializer
    permission_classes = [permissions.AllowAny]


class StudentTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['student_number'] = user.student_number
        return token


class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainSerializer


class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = StudentProfile.objects.get(user=request.user)
        return Response(StudentProfileSerializer(profile).data)