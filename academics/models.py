from django.db import models
from django.conf import settings


class Module(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    credits = models.PositiveSmallIntegerField(default=15)
    level = models.PositiveSmallIntegerField(help_text="Year level, e.g. 1-4")
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return self.code


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='enrollments')
    year = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=15,
        choices=[('active', 'Active'), ('passed', 'Passed'), ('failed', 'Failed')],
        default='active',
    )

    class Meta:
        unique_together = ('student', 'module', 'year')


class Mark(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='marks')
    assessment_name = models.CharField(max_length=100)
    weight_percent = models.DecimalField(max_digits=5, decimal_places=2)
    score_percent = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                     null=True, related_name='marks_uploaded')


class AttendanceRecord(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('enrollment', 'date')


class RiskAssessment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='risk_history')
    computed_at = models.DateTimeField(auto_now_add=True)
    risk_level = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    average_mark = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    attendance_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    modules_failed_count = models.PositiveSmallIntegerField(default=0)
    advice_text = models.TextField(blank=True)