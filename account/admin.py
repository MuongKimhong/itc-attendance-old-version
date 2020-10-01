from .forms import TeacherRegisterForm, StudentRegisterForm, EditUserForm
from .models import CustomUser, Teacher, Student
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    form = EditUserForm
    add_teacher_form = TeacherRegisterForm
    add_student_form = StudentRegisterForm
    list_display = (
        'email', 'first_name', 'last_name', 'gender', 'is_teacher', 'is_student',
        'phone', 'date_of_birth', 'is_staff', 'is_active',
    )
    list_filter = (
        'email', 'first_name', 'last_name', 'gender', 'is_teacher', 'is_student',
        'phone', 'date_of_birth', 'is_staff', 'is_active',
    )
    fieldsets = (
        (None, {'fields': (
            'email', 'password', 'first_name', 'last_name', 'gender', 'is_teacher', 'is_student',
            'phone', 'date_of_birth', 'department', 'years'
        )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'gender', 'is_teacher', 'is_student',
                'phone', 'password1', 'password2', 'is_staff', 'is_active',

            )}
         ),
    )
    search_fields = ('email', 'gender', 'is_teacher', 'is_student',
                     'phone')
    ordering = ('email', 'gender', 'is_teacher', 'is_student',
                'phone')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Teacher)
admin.site.register(Student)