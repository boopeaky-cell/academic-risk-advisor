from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'student_number', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'student_number')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)