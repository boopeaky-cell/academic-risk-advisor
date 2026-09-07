from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentRegisterView, StudentLoginView, MyProfileView

urlpatterns = [
    path('register/', StudentRegisterView.as_view(), name='student-register'),
    path('login/', StudentLoginView.as_view(), name='student-login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
]