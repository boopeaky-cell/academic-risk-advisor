from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    student_number = models.CharField(
        max_length=20, unique=True, null=True, blank=True,
        help_text="Required for students, blank for lecturers/admins"
    )

    def __str__(self):
        return self.student_number or self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    level_of_study = models.PositiveSmallIntegerField(help_text="e.g. 1, 2, 3, 4")
    programme = models.CharField(max_length=100, default="Computer Science")
    credits_completed = models.PositiveIntegerField(default=0)
    credits_required = models.PositiveIntegerField(default=360)
    current_risk_level = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='low',
    )

    def __str__(self):
        return f"{self.user.student_number} ({self.programme})"