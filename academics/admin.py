from django.contrib import admin
from .models import Module, Enrollment, Mark, AttendanceRecord, RiskAssessment

admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Mark)
admin.site.register(AttendanceRecord)
admin.site.register(RiskAssessment)